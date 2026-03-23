"""Core algorithm for finding shortest paths between Wikipedia pages."""

import copy

import networkx as nx
import wikipediaapi


def get_links(page):
    """Extract and return a sorted list of link titles from a WikipediaPage."""
    return sorted(page.links.keys())


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


def find_shortest_path(page_a_name, page_b_name, wiki=None, on_progress=None):
    """
    Find the shortest path between two Wikipedia pages.

    Args:
        page_a_name: Title of the first Wikipedia page.
        page_b_name: Title of the second Wikipedia page.
        wiki: Optional wikipediaapi.Wikipedia instance (for testing).
        on_progress: Optional callback(pages_explored, current_title) for UI updates.

    Returns:
        List of page titles forming the shortest path.

    Raises:
        ValueError: If either page does not exist or no path is found.
    """
    if wiki is None:
        wiki = wikipediaapi.Wikipedia("wikiviz/0.1.0", "en")

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
            return nx.shortest_path(G, page_a.title, page_b.title)
        except nx.NetworkXNoPath:
            continue

    raise ValueError(
        f"No path found between {page_a.title} and {page_b.title}"
    )
