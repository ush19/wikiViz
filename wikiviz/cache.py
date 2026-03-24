"""DuckDB-backed cache for Wikipedia page links."""

import json
from datetime import datetime, timedelta

import duckdb


_DEFAULT_DB_PATH = "wikiviz_cache.duckdb"
_DEFAULT_TTL_DAYS = 7


def get_connection(db_path=None):
    """Get a DuckDB connection, creating the cache table if needed."""
    path = db_path or _DEFAULT_DB_PATH
    conn = duckdb.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS link_cache (
            page_title TEXT PRIMARY KEY,
            links JSON NOT NULL,
            fetched_at TIMESTAMP NOT NULL
        )
    """)
    return conn


def get_cached_links(conn, title, ttl_days=_DEFAULT_TTL_DAYS):
    """
    Look up cached links for a page title.

    Returns a list of link titles if cached and not expired, else None.
    """
    cutoff = datetime.now() - timedelta(days=ttl_days)
    result = conn.execute(
        "SELECT links FROM link_cache WHERE page_title = ? AND fetched_at > ?",
        [title, cutoff],
    ).fetchone()
    if result is None:
        return None
    return json.loads(result[0])


def set_cached_links(conn, title, links):
    """Store links for a page title in the cache."""
    conn.execute(
        """
        INSERT OR REPLACE INTO link_cache (page_title, links, fetched_at)
        VALUES (?, ?, ?)
        """,
        [title, json.dumps(links), datetime.now()],
    )


def get_cache_stats(conn):
    """Return cache statistics."""
    row = conn.execute("SELECT COUNT(*) FROM link_cache").fetchone()
    return {"total_pages": row[0]}
