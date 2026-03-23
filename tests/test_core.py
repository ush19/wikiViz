import pytest
from unittest.mock import MagicMock, patch
from wikiviz.core import (
    get_links, clean_links, find_shortest_path,
    get_content_links, page_exists, _get_sections, _get_links_for_section,
)


# --- Mock helpers ---

def _make_mock_wiki(page_links):
    """
    Helper: create a mock wikipediaapi.Wikipedia instance.
    page_links is a dict like {"PageA": ["PageB", "PageC"], "PageB": ["PageD"]}.
    """
    mock_wiki = MagicMock()

    def mock_page(title):
        page = MagicMock()
        page.title = title
        page.exists.return_value = title in page_links
        links_dict = {link: MagicMock() for link in page_links.get(title, [])}
        page.links = links_dict
        return page

    mock_wiki.page = mock_page
    return mock_wiki


# --- get_links (legacy) ---

def test_get_links():
    """get_links should return a sorted list of link titles from a WikipediaPage."""
    mock_page = MagicMock()
    mock_page.links = {
        "Zebra": MagicMock(),
        "Apple": MagicMock(),
        "Mango": MagicMock(),
    }

    result = get_links(mock_page)

    assert result == ["Apple", "Mango", "Zebra"]


# --- clean_links ---

def test_clean_links_removes_metadata():
    """clean_links should filter out Wikipedia metadata links."""
    links = [
        "Albert Einstein",
        "Category:Physics",
        "File:Einstein.jpg",
        "Help:Contents",
        "List of physicists",
        "Physics (disambiguation)",
        "Portal:Science",
        "Quantum mechanics",
        "Talk:Physics",
        "Template:Physics",
        "Template talk:Physics",
        "Wayback Machine",
        "Wikipedia:About",
        "WikiProject Physics",
        "Specials (Unicode block)",
        "ISSN (identifier)",
    ]

    result = clean_links(links)

    assert result == ["Albert Einstein", "Quantum mechanics"]


def test_clean_links_preserves_normal_articles():
    """clean_links should not filter out regular article titles."""
    links = ["Python (programming language)", "Machine learning", "Data science"]

    result = clean_links(links)

    assert result == ["Python (programming language)", "Machine learning", "Data science"]


# --- get_content_links ---

def _mock_sections_response(sections):
    """Create a mock response for the sections API call."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {
        "parse": {
            "title": "Test",
            "sections": sections,
        }
    }
    return resp


def _mock_links_response(links):
    """Create a mock response for the links API call."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {
        "parse": {
            "links": [{"ns": 0, "*": title, "exists": ""} for title in links]
        }
    }
    return resp


def test_get_content_links_skips_references():
    """get_content_links should skip links from non-content sections."""
    session = MagicMock()

    sections = [
        {"toclevel": 1, "level": "2", "line": "History", "index": "1"},
        {"toclevel": 1, "level": "2", "line": "Geography", "index": "2"},
        {"toclevel": 1, "level": "2", "line": "See also", "index": "3"},
        {"toclevel": 1, "level": "2", "line": "References", "index": "4"},
    ]

    def mock_get(url, params=None, headers=None):
        if params.get("prop") == "sections":
            return _mock_sections_response(sections)
        elif params.get("prop") == "links":
            section = params.get("section", "0")
            if section == "0":
                return _mock_links_response(["Intro Link"])
            elif section == "1":
                return _mock_links_response(["History Link"])
            elif section == "2":
                return _mock_links_response(["Geography Link"])
            elif section == "3":
                return _mock_links_response(["See Also Link"])
            elif section == "4":
                return _mock_links_response(["Reference Link"])
        return MagicMock()

    session.get = mock_get

    result = get_content_links("Test", session=session)

    assert "Intro Link" in result
    assert "History Link" in result
    assert "Geography Link" in result
    assert "See Also Link" not in result
    assert "Reference Link" not in result


def test_get_content_links_returns_sorted_unique():
    """get_content_links should return sorted, deduplicated links."""
    session = MagicMock()

    sections = [
        {"toclevel": 1, "level": "2", "line": "Section A", "index": "1"},
    ]

    def mock_get(url, params=None, headers=None):
        if params.get("prop") == "sections":
            return _mock_sections_response(sections)
        elif params.get("prop") == "links":
            section = params.get("section", "0")
            if section == "0":
                return _mock_links_response(["Zebra", "Apple"])
            elif section == "1":
                return _mock_links_response(["Apple", "Mango"])  # Apple is duplicate
        return MagicMock()

    session.get = mock_get

    result = get_content_links("Test", session=session)

    assert result == ["Apple", "Mango", "Zebra"]


# --- page_exists ---

def test_page_exists_true():
    """page_exists should return True for existing pages."""
    session = MagicMock()
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {"query": {"pages": {"12345": {"title": "India"}}}}
    session.get.return_value = resp

    assert page_exists("India", session=session) is True


def test_page_exists_false():
    """page_exists should return False for nonexistent pages."""
    session = MagicMock()
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {"query": {"pages": {"-1": {"title": "Xyzzy123", "missing": ""}}}}
    session.get.return_value = resp

    assert page_exists("Xyzzy123", session=session) is False


# --- find_shortest_path (legacy mock path) ---

def test_find_shortest_path_direct():
    """find_shortest_path should find a direct connection (1 degree)."""
    wiki = _make_mock_wiki({
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": [],
        "D": [],
    })

    path = find_shortest_path("A", "B", wiki=wiki)

    assert path[0] == "A"
    assert path[-1] == "B"
    assert len(path) == 2


def test_find_shortest_path_no_connection():
    """find_shortest_path should raise ValueError when no path exists."""
    wiki = _make_mock_wiki({
        "Island1": ["Palm"],
        "Island2": ["Coconut"],
        "Palm": [],
        "Coconut": [],
    })

    with pytest.raises(ValueError, match="No path found"):
        find_shortest_path("Island1", "Island2", wiki=wiki)


def test_find_shortest_path_invalid_page():
    """find_shortest_path should raise ValueError for nonexistent pages."""
    wiki = _make_mock_wiki({})  # no pages exist

    with pytest.raises(ValueError, match="Page not found"):
        find_shortest_path("Nonexistent Page", "Another Fake", wiki=wiki)
