# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

wikiViz is a Wikipedia degrees-of-separation calculator. It finds the shortest path between two Wikipedia pages by iteratively fetching page links, building a NetworkX directed graph, and running `shortest_path()`.

Live app: https://wikiviz.streamlit.app/

## Development Setup

```bash
# Install in development mode (includes pytest)
pip install -e ".[dev]"

# Run tests
pytest

# Run the Streamlit web app
streamlit run main.py
```

## Project Structure

```
wikiviz/          # Python package — core logic + Streamlit app
  core.py         # get_links, clean_links, find_shortest_path (no UI deps)
  app.py          # Streamlit UI (thin wrapper over core)
tests/
  test_core.py    # pytest tests (mocked Wikipedia API, no network calls)
main.py           # Entry point: streamlit run main.py
notebooks/        # Reference Jupyter notebooks (read-only artifacts)
_archive/         # Legacy files preserved from original repo structure
```

## Architecture

### wikiviz/core.py

- `get_links(page)` — returns sorted list of link titles from a WikipediaPage
- `clean_links(links)` — filters out non-article Wikipedia links (categories, templates, etc.)
- `find_shortest_path(page_a_name, page_b_name, wiki=None)` — orchestrates the full algorithm. Accepts optional `wiki` param for dependency injection in tests. Raises `ValueError` for invalid pages or no path found.

### Data Flow

```
User Input (Page A, Page B)
  → Validate pages exist
  → Extract & clean links from both
  → Build graph dict, iteratively expand by fetching linked pages
  → Check nx.shortest_path() after each expansion
  → Return path list or raise ValueError
```

## Deployment

Streamlit Cloud reads `requirements.txt` at repo root (not `pyproject.toml`). Deploy from main branch only.

## Known Issues

- Graph direction is incorrect (A → B ← B instead of A → B)
- Network visualization not yet implemented
- API rate limiting on Streamlit Cloud
