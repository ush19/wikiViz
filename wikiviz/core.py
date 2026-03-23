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
