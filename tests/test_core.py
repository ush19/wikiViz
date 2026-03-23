from unittest.mock import MagicMock
from wikiviz.core import get_links, clean_links


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
