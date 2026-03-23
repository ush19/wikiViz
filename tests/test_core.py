import pytest
from unittest.mock import MagicMock
from wikiviz.core import get_links, clean_links, find_shortest_path


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
