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
├── docs/                           # Design specs and documentation
│   └── superpowers/specs/
└── .gitignore                      # Python + macOS ignores
```

## Component Design

### wikiviz/core.py

Extracted from `front-end-implementation/wikiviz-app.py`. Contains all algorithm logic with no Streamlit dependency.

**Functions:**

- `get_links(page)` — extract and sort all links from a `wikipediaapi.WikipediaPage`. Returns a new sorted list of link titles (refactored from the original `return_links` which mutated a list in-place).
- `clean_links(links)` — filter out non-article Wikipedia links (disambiguation, categories, templates, portal pages, etc.). Returns a new cleaned list.
- `find_shortest_path(page_a_name, page_b_name, wiki=None)` — orchestrates the full algorithm. Accepts an optional `wikipediaapi.Wikipedia` instance for dependency injection (defaults to creating one with user-agent `"wikiviz/0.1.0"`).
  1. Validate both pages exist via `page.exists()`; raise `ValueError` if either does not
  2. Extract and clean links from both
  3. Build initial graph dict `{title: [links]}` (uses `copy.deepcopy` to avoid mutation issues)
  4. Iteratively expand graph by fetching links from discovered pages
  5. After each expansion, convert to NetworkX graph and check `nx.shortest_path()`
  6. Return the path as a list of page titles on success
  7. Raise `ValueError` if no path is found after exhausting iterations

### wikiviz/app.py

Streamlit UI code. Imports from `wikiviz.core`. Handles:
- Form input (two Wikipedia page names)
- Calls `find_shortest_path()`, catches `ValueError` to display error messages
- Displays results
- Logs to file (using `with` statements for file handling)

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
| `.ipynb_checkpoints/` | Remove from tracking | Add to `.gitignore` |
| `.DS_Store` | Remove from tracking | Add to `.gitignore` |

## Packaging

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "wikiviz"
version = "0.1.0"
description = "Wikipedia degrees of separation calculator"
requires-python = ">=3.9"
license = "MIT"
dependencies = [
    "Wikipedia-API>=0.6.0",
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

2. **`test_get_links`** — mock `wikipediaapi.WikipediaPage` to return known links. Assert correct extraction and sorting.

3. **`test_find_shortest_path`** — mock `wikipediaapi.Wikipedia` via dependency injection. Mock pages return controlled link sets forming A->B->C->D. Assert path is `["A", "B", "C", "D"]`.

4. **`test_find_shortest_path_no_connection`** — mock two disconnected subgraphs. Assert `ValueError` is raised.

5. **`test_find_shortest_path_invalid_page`** — mock a page where `exists()` returns `False`. Assert `ValueError` is raised.

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
