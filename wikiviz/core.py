"""Core algorithm for finding shortest paths between Wikipedia pages."""

import copy

import networkx as nx
import requests

_API_URL = "https://en.wikipedia.org/w/api.php"
_USER_AGENT = "wikiviz/0.1.0"

_EXCLUDE_SECTIONS = frozenset({
    "See also", "Notes", "References", "Bibliography",
    "External links", "Further reading", "Sources",
})

_EXCLUDE_EXACT = {"Wayback Machine", "Specials (Unicode block)"}
_EXCLUDE_SUFFIXES = ("(disambiguation)", "(identifier)")
_EXCLUDE_PREFIXES = (
    "List of ", "Category:", "File:", "Help:", "Talk:",
    "Template:", "Wikipedia:", "Template talk:", "Portal:", "Wiki",
)


def clean_links(links):
    """Filter out non-article Wikipedia links. Returns a new list."""
    return [
        link for link in links
        if link not in _EXCLUDE_EXACT
        and not link.endswith(_EXCLUDE_SUFFIXES)
        and not link.startswith(_EXCLUDE_PREFIXES)
    ]


def _get_sections(title, session=None):
    """Fetch section list for a Wikipedia page. Returns list of {index, title} dicts."""
    s = session or requests.Session()
    resp = s.get(_API_URL, params={
        "action": "parse",
        "page": title,
        "prop": "sections",
        "format": "json",
    }, headers={"User-Agent": _USER_AGENT})
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        return None
    return data["parse"]["sections"]


def _get_links_for_section(title, section_index, session=None):
    """Fetch article links (namespace 0) for a specific section of a page."""
    s = session or requests.Session()
    resp = s.get(_API_URL, params={
        "action": "parse",
        "page": title,
        "section": str(section_index),
        "prop": "links",
        "format": "json",
    }, headers={"User-Agent": _USER_AGENT})
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        return []
    return [
        link["*"] for link in data["parse"]["links"]
        if link.get("ns", -1) == 0 and "exists" in link
    ]


def page_exists(title, session=None):
    """Check if a Wikipedia page exists using the MediaWiki API."""
    s = session or requests.Session()
    resp = s.get(_API_URL, params={
        "action": "query",
        "titles": title,
        "format": "json",
    }, headers={"User-Agent": _USER_AGENT})
    resp.raise_for_status()
    pages = resp.json()["query"]["pages"]
    return "-1" not in pages


def get_content_links(title, session=None):
    """
    Fetch links from content sections of a Wikipedia page only.

    Skips non-content sections (See also, References, Bibliography, etc.)
    to reduce noise in the graph.

    Returns a sorted list of unique article link titles.
    """
    s = session or requests.Session()
    sections = _get_sections(title, session=s)
    if sections is None:
        return []

    # Collect indices of sections to exclude (and their children)
    exclude_indices = set()
    for sec in sections:
        if sec["line"] in _EXCLUDE_SECTIONS:
            exclude_indices.add(int(sec["index"]))

    # Build set of child sections to exclude (anything nested under excluded parent)
    all_exclude = set()
    for sec in sections:
        idx = int(sec["index"])
        if idx in exclude_indices:
            all_exclude.add(idx)
        else:
            # Check if any ancestor is excluded by comparing toclevel
            for ex_idx in exclude_indices:
                ex_sec = next((s for s in sections if int(s["index"]) == ex_idx), None)
                if ex_sec and int(ex_sec["toclevel"]) < int(sec["toclevel"]) and idx > ex_idx:
                    # Check if there's no same-or-higher-level section between ex_idx and idx
                    is_child = True
                    for between in sections:
                        b_idx = int(between["index"])
                        if ex_idx < b_idx < idx and int(between["toclevel"]) <= int(ex_sec["toclevel"]):
                            is_child = False
                            break
                    if is_child:
                        all_exclude.add(idx)

    # Fetch links from intro (section 0) + content sections
    all_links = set()

    # Section 0 = intro (before first heading)
    intro_links = _get_links_for_section(title, 0, session=s)
    all_links.update(intro_links)

    for sec in sections:
        idx = int(sec["index"])
        if idx not in all_exclude:
            sec_links = _get_links_for_section(title, idx, session=s)
            all_links.update(sec_links)

    return sorted(all_links)


# Keep old get_links for backward compatibility with tests that use mock WikipediaPage objects
def get_links(page):
    """Extract and return a sorted list of link titles from a WikipediaPage."""
    return sorted(page.links.keys())


def find_shortest_path(page_a_name, page_b_name, wiki=None, on_progress=None,
                       session=None):
    """
    Find the shortest path between two Wikipedia pages.

    Uses MediaWiki API with section-aware link fetching to skip
    non-content sections (References, Bibliography, See also, etc.).

    Args:
        page_a_name: Title of the first Wikipedia page.
        page_b_name: Title of the second Wikipedia page.
        wiki: Optional wikipediaapi.Wikipedia instance (for testing with mocks).
        on_progress: Optional callback(pages_explored, current_title) for UI updates.
        session: Optional requests.Session for connection reuse.

    Returns:
        Tuple of (path, graph) where path is a list of page titles forming
        the shortest path, and graph is a dict {title: [links]} of all
        explored pages.

    Raises:
        ValueError: If either page does not exist or no path is found.
    """
    # If a mock wiki is passed (testing), use the old code path
    if wiki is not None:
        return _find_shortest_path_legacy(page_a_name, page_b_name, wiki, on_progress)

    s = session or requests.Session()

    if not page_exists(page_a_name, session=s):
        raise ValueError(f"Page not found: {page_a_name}")
    if not page_exists(page_b_name, session=s):
        raise ValueError(f"Page not found: {page_b_name}")

    links_a = clean_links(get_content_links(page_a_name, session=s))
    links_b = clean_links(get_content_links(page_b_name, session=s))

    graph = {
        page_a_name: links_a,
        page_b_name: links_b,
    }

    titles = links_a + links_b

    for i, t in enumerate(titles):
        if on_progress:
            on_progress(i + 1, t)

        page_links = clean_links(get_content_links(t, session=s))

        graph[t] = copy.deepcopy(page_links)

        for p in page_links:
            if p not in titles:
                titles.append(p)
            else:
                break
            break

        try:
            G = nx.to_networkx_graph(graph)
            path = nx.shortest_path(G, page_a_name, page_b_name)
            return path, graph
        except nx.NetworkXNoPath:
            continue

    raise ValueError(
        f"No path found between {page_a_name} and {page_b_name}"
    )


def _find_shortest_path_legacy(page_a_name, page_b_name, wiki, on_progress=None):
    """Legacy path finder using wikipediaapi mock objects (for testing)."""
    page_a = wiki.page(page_a_name)
    page_b = wiki.page(page_b_name)

    if not page_a.exists():
        raise ValueError(f"Page not found: {page_a_name}")
    if not page_b.exists():
        raise ValueError(f"Page not found: {page_b_name}")

    links_a = clean_links(get_links(page_a))
    links_b = clean_links(get_links(page_b))

    graph = {
        page_a.title: links_a,
        page_b.title: links_b,
    }

    titles = links_a + links_b

    for i, t in enumerate(titles):
        if on_progress:
            on_progress(i + 1, t)

        page = wiki.page(t)
        page_links = clean_links(get_links(page))

        graph[page.title] = copy.deepcopy(page_links)

        for p in page_links:
            if p not in titles:
                titles.append(p)
            else:
                break
            break

        try:
            G = nx.to_networkx_graph(graph)
            path = nx.shortest_path(G, page_a.title, page_b.title)
            return path, graph
        except nx.NetworkXNoPath:
            continue

    raise ValueError(
        f"No path found between {page_a.title} and {page_b.title}"
    )
