from unittest.mock import MagicMock
from wikiviz.core import get_links


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
