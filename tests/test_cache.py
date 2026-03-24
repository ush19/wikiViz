import duckdb
import pytest
from wikiviz.cache import get_connection, get_cached_links, set_cached_links, get_cache_stats


@pytest.fixture
def cache_conn():
    """Create an in-memory DuckDB cache for testing."""
    conn = get_connection(":memory:")
    yield conn
    conn.close()


def test_set_and_get_cached_links(cache_conn):
    """Cached links should be retrievable after storing."""
    links = ["Apple", "Banana", "Cherry"]
    set_cached_links(cache_conn, "Fruit", links)

    result = get_cached_links(cache_conn, "Fruit")

    assert result == ["Apple", "Banana", "Cherry"]


def test_get_cached_links_miss(cache_conn):
    """Uncached pages should return None."""
    result = get_cached_links(cache_conn, "Nonexistent")

    assert result is None


def test_cache_overwrites_on_update(cache_conn):
    """Storing links for the same page should overwrite the old entry."""
    set_cached_links(cache_conn, "Fruit", ["Apple"])
    set_cached_links(cache_conn, "Fruit", ["Apple", "Banana"])

    result = get_cached_links(cache_conn, "Fruit")

    assert result == ["Apple", "Banana"]


def test_get_cache_stats(cache_conn):
    """Cache stats should reflect the number of cached pages."""
    assert get_cache_stats(cache_conn)["total_pages"] == 0

    set_cached_links(cache_conn, "Page1", ["A"])
    set_cached_links(cache_conn, "Page2", ["B"])

    assert get_cache_stats(cache_conn)["total_pages"] == 2


def test_expired_cache_returns_none(cache_conn):
    """Links older than TTL should not be returned."""
    set_cached_links(cache_conn, "Old", ["A"])

    # Manually backdate the fetched_at timestamp
    cache_conn.execute(
        "UPDATE link_cache SET fetched_at = '2020-01-01' WHERE page_title = 'Old'"
    )

    result = get_cached_links(cache_conn, "Old", ttl_days=7)

    assert result is None
