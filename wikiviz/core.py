"""Core algorithm for finding shortest paths between Wikipedia pages."""

import copy

import networkx as nx
import wikipediaapi


def get_links(page):
    """Extract and return a sorted list of link titles from a WikipediaPage."""
    return sorted(page.links.keys())
