# Formalize wikiViz Repo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure wikiViz from loose scripts/notebooks into a proper Python package with pyproject.toml, MIT license, tests, and clean directory layout.

**Architecture:** Extract core algorithm from `front-end-implementation/wikiviz-app.py` into `wikiviz/core.py` (pure logic, no UI). Streamlit UI goes to `wikiviz/app.py`. Legacy files move to `_archive/` and `notebooks/`. TDD for the core module.

**Tech Stack:** Python 3.9+, Wikipedia-API, NetworkX, Streamlit, pytest

**Spec:** `docs/superpowers/specs/2026-03-23-formalize-repo-design.md`

---

### Task 1: Scaffold project structure and packaging

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `wikiviz/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create `.gitignore`**

```
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
*.egg
.ipynb_checkpoints/
.DS_Store
*.swp
.env
.venv/
```

- [ ] **Step 2: Create `pyproject.toml`**

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

- [ ] **Step 3: Create `LICENSE` (MIT)**

```
MIT License

Copyright (c) 2022 Susheel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 4: Create `wikiviz/__init__.py`**

```python
"""wikiviz — Wikipedia degrees of separation calculator."""

__version__ = "0.1.0"
```

- [ ] **Step 5: Create `tests/__init__.py`**

Empty file.

- [ ] **Step 6: Commit**

```bash
git add .gitignore pyproject.toml LICENSE wikiviz/__init__.py tests/__init__.py
git commit -m "scaffold: add pyproject.toml, LICENSE, .gitignore, package stubs"
```

---

### Task 2: Move legacy files to `_archive/` and `notebooks/`

**Files:**
- Move: `front-end-implementation/` → `_archive/front-end-implementation/`
- Move: `reference/` → `_archive/reference/`
- Move: `test result files/` → `_archive/test result files/`
- Move: `.spyproject/` → `_archive/.spyproject/`
- Move: `run_logs.txt` → `_archive/run_logs.txt`
- Move: `wikiviz.ipynb` → `notebooks/wikiviz.ipynb`
- Move: `scrap_wiki_scraper.ipynb` → `notebooks/scrap_wiki_scraper.ipynb`
- Remove from tracking: `.ipynb_checkpoints/`, `.DS_Store`

- [ ] **Step 1: Create directories**

```bash
mkdir -p _archive notebooks
```

- [ ] **Step 2: Move files with git**

```bash
git mv front-end-implementation _archive/front-end-implementation
git mv reference _archive/reference
git mv "test result files" "_archive/test result files"
git mv .spyproject _archive/.spyproject
git mv run_logs.txt _archive/run_logs.txt
git mv wikiviz.ipynb notebooks/wikiviz.ipynb
git mv scrap_wiki_scraper.ipynb notebooks/scrap_wiki_scraper.ipynb
```

- [ ] **Step 3: Remove `.ipynb_checkpoints/` and `.DS_Store` from tracking**

```bash
git rm -r --cached .ipynb_checkpoints
git rm --cached .DS_Store
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "restructure: move legacy files to _archive/ and notebooks/"
```

---

### Task 3: Implement `wikiviz/core.py` with TDD — `get_links`

**Files:**
- Create: `wikiviz/core.py`
- Create: `tests/test_core.py`

- [ ] **Step 1: Write failing test for `get_links`**

```python
# tests/test_core.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_core.py::test_get_links -v`
Expected: FAIL — `ImportError: cannot import name 'get_links'`

- [ ] **Step 3: Write minimal implementation**

```python
# wikiviz/core.py
"""Core algorithm for finding shortest paths between Wikipedia pages."""

import copy

import networkx as nx
import wikipediaapi


def get_links(page):
    """Extract and return a sorted list of link titles from a WikipediaPage."""
    return sorted(page.links.keys())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_core.py::test_get_links -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add wikiviz/core.py tests/test_core.py
git commit -m "feat: add get_links with test"
```

---

### Task 4: Implement `clean_links` with TDD

**Files:**
- Modify: `wikiviz/core.py`
- Modify: `tests/test_core.py`

- [ ] **Step 1: Write failing test for `clean_links`**

Append to `tests/test_core.py`:

```python
from wikiviz.core import get_links, clean_links


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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core.py -k "clean_links" -v`
Expected: FAIL — `ImportError: cannot import name 'clean_links'`

- [ ] **Step 3: Write minimal implementation**

Add to `wikiviz/core.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core.py -k "clean_links" -v`
Expected: PASS (both tests)

- [ ] **Step 5: Commit**

```bash
git add wikiviz/core.py tests/test_core.py
git commit -m "feat: add clean_links with tests"
```

---

### Task 5: Implement `find_shortest_path` with TDD

**Files:**
- Modify: `wikiviz/core.py`
- Modify: `tests/test_core.py`

- [ ] **Step 1: Write failing test for `find_shortest_path` — happy path**

Append to `tests/test_core.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_core.py::test_find_shortest_path_direct -v`
Expected: FAIL — `ImportError: cannot import name 'find_shortest_path'`

- [ ] **Step 3: Write implementation**

Add to `wikiviz/core.py`:

```python
def find_shortest_path(page_a_name, page_b_name, wiki=None):
    """
    Find the shortest path between two Wikipedia pages.

    Args:
        page_a_name: Title of the first Wikipedia page.
        page_b_name: Title of the second Wikipedia page.
        wiki: Optional wikipediaapi.Wikipedia instance (for testing).

    Returns:
        List of page titles forming the shortest path.

    Raises:
        ValueError: If either page does not exist or no path is found.
    """
    if wiki is None:
        wiki = wikipediaapi.Wikipedia("wikiviz/0.1.0", "en")

    page_a = wiki.page(page_a_name)
    page_b = wiki.page(page_b_name)

    if not page_a.exists():
        raise ValueError(f"Page not found: {page_a_name}")
    if not page_b.exists():
        raise ValueError(f"Page not found: {page_b_name}")

    links_a = clean_links(get_links(page_a))
    links_b = clean_links(get_links(page_b))

    graph = {
        page_a.title: links_a,
        page_b.title: links_b,
    }

    titles = links_a + links_b

    for t in titles:
        page = wiki.page(t)
        page_links = clean_links(get_links(page))

        graph[page.title] = copy.deepcopy(page_links)

        for p in page_links:
            if p not in titles:
                titles.append(p)
            else:
                break
            break

        try:
            G = nx.to_networkx_graph(graph)
            return nx.shortest_path(G, page_a.title, page_b.title)
        except nx.NetworkXNoPath:
            continue

    raise ValueError(
        f"No path found between {page_a.title} and {page_b.title}"
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_core.py::test_find_shortest_path_direct -v`
Expected: PASS

- [ ] **Step 5: Write failing test — no connection**

Append to `tests/test_core.py`:

```python
import pytest


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
```

- [ ] **Step 6: Run test to verify it passes**

Run: `pytest tests/test_core.py::test_find_shortest_path_no_connection -v`
Expected: PASS (the implementation already raises ValueError)

- [ ] **Step 7: Write failing test — invalid page**

Append to `tests/test_core.py`:

```python
def test_find_shortest_path_invalid_page():
    """find_shortest_path should raise ValueError for nonexistent pages."""
    wiki = _make_mock_wiki({})  # no pages exist

    with pytest.raises(ValueError, match="Page not found"):
        find_shortest_path("Nonexistent Page", "Another Fake", wiki=wiki)
```

- [ ] **Step 8: Run test to verify it passes**

Run: `pytest tests/test_core.py::test_find_shortest_path_invalid_page -v`
Expected: PASS

- [ ] **Step 9: Run full test suite**

Run: `pytest tests/ -v`
Expected: All 7 tests PASS

- [ ] **Step 10: Commit**

```bash
git add wikiviz/core.py tests/test_core.py
git commit -m "feat: add find_shortest_path with tests"
```

---

### Task 6: Implement `wikiviz/app.py` and `main.py`

**Files:**
- Create: `wikiviz/app.py`
- Create: `main.py`

- [ ] **Step 1: Create `wikiviz/app.py`**

```python
"""Streamlit UI for wikiViz."""

from datetime import datetime

import streamlit as st

from wikiviz.core import find_shortest_path


def main():
    st.title("Degrees of Separation: Wikipedia Edition")

    st.write(
        "Give me any two Wikipedia pages and I'll tell you how many "
        "and what Wiki pages connect those two pages"
    )

    st.write(
        "If you see errors below, please try at another time. "
        "The API cannot handle too many requests."
    )

    with st.form(key="my_form_to_submit"):
        search_node_a = st.text_input("Enter first Wikipedia page name: ", "")
        search_node_b = st.text_input("Enter second Wikipedia page name: ", "")
        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        now = datetime.now()

        try:
            path = find_shortest_path(search_node_a, search_node_b)
            degrees = len(path) - 1
            output = (
                f"There are {degrees} degrees of separation between "
                f"{path[0]} and {path[-1]}\n\n{path}"
            )
        except ValueError as e:
            output = str(e)

        st.write(output)

        with open("app_run_logs.txt", "a") as log:
            log.write(f"{output}\n")
            log.write(f"Run: {now}\n\n")
```

- [ ] **Step 2: Create `main.py`**

```python
from wikiviz.app import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Verify import works**

Run: `python -c "from wikiviz.app import main; print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add wikiviz/app.py main.py
git commit -m "feat: add Streamlit app and main entry point"
```

---

### Task 7: Update CLAUDE.md and README.md

**Files:**
- Modify: `CLAUDE.md`
- Modify: `README.md`

- [ ] **Step 1: Update `CLAUDE.md`** to reflect new structure, commands, and architecture.

- [ ] **Step 2: Update `README.md`** — add installation instructions, license badge, updated project description reflecting the new structure.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md README.md
git commit -m "docs: update CLAUDE.md and README.md for new project structure"
```

---

### Task 8: Install, run tests, verify everything works

- [ ] **Step 1: Install in dev mode**

Run: `pip install -e ".[dev]"`
Expected: Successful install

- [ ] **Step 2: Run full test suite**

Run: `pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 3: Verify Streamlit app can start**

Run: `timeout 10 streamlit run main.py --server.headless true 2>&1 || true`
Expected: Streamlit starts without import errors

- [ ] **Step 4: Final commit if any fixes needed**
