# Formalize wikiViz Repository

## Summary

Restructure the wikiViz project from a loose collection of scripts and notebooks into a proper Python package with modern packaging (`pyproject.toml`), MIT licensing, a clean directory layout, pytest-based tests, and an `_archive/` for legacy files.

## Project Structure

```
wikiViz/
├── wikiviz/                        # Importable Python package
│   ├── __init__.py                 # Package metadata (version, etc.)
│   ├── core.py                     # return_links, clean_links, find_shortest_path
│   └── app.py                      # Streamlit UI (thin layer over core)
├── tests/
│   ├── __init__.py
│   └── test_core.py                # pytest tests for core functions
├── notebooks/                      # Reference artifacts (read-only)
│   ├── wikiviz.ipynb
│   └── scrap_wiki_scraper.ipynb
├── _archive/                       # Legacy files, preserved but out of the way
│   ├── front-end-implementation/
│   ├── reference/
│   ├── test result files/
│   ├── .spyproject/
│   └── run_logs.txt
├── main.py                         # Entry point: `streamlit run main.py`
├── pyproject.toml                  # Build system, deps, dev extras
├── LICENSE                         # MIT
├── README.md                       # Updated
├── CLAUDE.md                       # Updated
└── .gitignore                      # Python-standard ignores
```

## Component Design

### wikiviz/core.py

Extracted from `front-end-implementation/wikiviz-app.py`. Contains all algorithm logic with no Streamlit dependency.

**Functions:**

- `return_links(page, list_n)` — extract and sort all links from a Wikipedia page. Takes a `wikipediaapi.WikipediaPage` and a list to append to. Returns the updated list.
- `clean_links(list_node)` — filter out non-article Wikipedia links (disambiguation, categories, templates, portal pages, etc.). Returns cleaned list.
- `find_shortest_path(page_a_name, page_b_name)` — orchestrates the full algorithm:
  1. Fetch both pages via Wikipedia-API
  2. Extract and clean links from both
  3. Build initial graph dict `{title: [links]}`
  4. Iteratively expand graph by fetching links from discovered pages
  5. After each expansion, convert to NetworkX graph and check `nx.shortest_path()`
  6. Return the path as a list of page titles, or raise/return appropriate error if no path found

### wikiviz/app.py

Streamlit UI code. Imports from `wikiviz.core`. Handles:
- Form input (two Wikipedia page names)
- Calls `find_shortest_path()`
- Displays results
- Logs to file

### main.py

Thin entry point:
```python
from wikiviz.app import main

if __name__ == "__main__":
    main()
```

Run with: `streamlit run main.py`

## File Migration Plan

| Current Location | Destination | Action |
|---|---|---|
| `front-end-implementation/wikiviz-app.py` | `wikiviz/core.py` + `wikiviz/app.py` | Extract and split |
| `front-end-implementation/wikiviz-main.py` | `_archive/front-end-implementation/` | Archive |
| `front-end-implementation/requirements.txt` | Replaced by `pyproject.toml` | Archive original |
| `front-end-implementation/streamlit-commands.txt` | `_archive/front-end-implementation/` | Archive |
| `front-end-implementation/app_run_logs.txt` | `_archive/front-end-implementation/` | Archive |
| `wikiviz.ipynb` | `notebooks/wikiviz.ipynb` | Move |
| `scrap_wiki_scraper.ipynb` | `notebooks/scrap_wiki_scraper.ipynb` | Move |
| `reference/` | `_archive/reference/` | Move |
| `test result files/` | `_archive/test result files/` | Move |
| `run_logs.txt` | `_archive/run_logs.txt` | Move |
| `.spyproject/` | `_archive/.spyproject/` | Move |

## Packaging

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "wikiviz"
version = "0.1.0"
description = "Wikipedia degrees of separation calculator"
requires-python = ">=3.9"
license = "MIT"
dependencies = [
    "Wikipedia-API>=0.5.4",
    "networkx>=2.5",
    "streamlit>=1.16.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0"]
```

### Development Setup

```bash
pip install -e ".[dev]"
```

## Testing Strategy

All tests in `tests/test_core.py` using pytest. Mock the Wikipedia API at the network boundary — no live HTTP calls.

### Test Cases

1. **`test_clean_links`** — pass a list with real article titles mixed with Wikipedia metadata links (disambiguation, categories, templates). Assert only article titles survive.

2. **`test_return_links`** — mock `wikipediaapi.WikipediaPage` to return known links. Assert correct extraction and sorting.

3. **`test_find_shortest_path`** — build a small NetworkX graph by hand (A->B->C->D), call `find_shortest_path` with mocked Wikipedia API that returns these connections. Assert path is `["A", "B", "C", "D"]`.

4. **`test_find_shortest_path_no_connection`** — mock two disconnected subgraphs. Assert appropriate error/result when no path exists.

### Running Tests

```bash
pytest
```

## License

MIT License, copyright holder: Susheel (from existing git history).

## Out of Scope

- Fixing the graph direction bug (A->B<-B) — tracked as a known issue
- Implementing network visualization
- Streamlit Cloud deployment configuration
- R implementation
- CLI command wrapping `streamlit run`
