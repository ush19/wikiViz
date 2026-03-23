# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

wikiViz is a Wikipedia degrees-of-separation calculator. It finds the shortest path between two Wikipedia pages by iteratively fetching page links, building a NetworkX directed graph, and running `shortest_path()`.

Live app: https://ush19-wikiviz-front-end-implementationwikiviz-app-jvy70i.streamlit.app/

## Running the Application

```bash
# Install dependencies
pip install -r front-end-implementation/requirements.txt

# Run the Streamlit web app
streamlit run front-end-implementation/wikiviz-app.py

# Run the CLI version (no web UI, same algorithm)
python front-end-implementation/wikiviz-main.py
```

## Dependencies

- **Wikipedia-API 0.5.4** — fetches Wikipedia page content and links
- **NetworkX 2.5** — graph construction and shortest path algorithm
- **Streamlit 1.16.0** — web UI

## Architecture

### Core Algorithm (shared by wikiviz-app.py and wikiviz-main.py)

1. **`return_links(page, list_n)`** — extracts and sorts all links from a Wikipedia page
2. **`clean_links(list_node)`** — filters out non-article links (disambiguation, categories, templates, Wikipedia metadata)
3. **Path finding loop** — fetches links from both input pages, combines them, then iteratively expands the graph by fetching links from discovered pages. After each expansion, checks `nx.shortest_path()` for a connection. Catches `NetworkXNoPath` to continue iteration.

### Data Flow

```
User Input (Page A, Page B)
  → Fetch pages via wikipediaapi
  → Extract & clean links
  → Build initial graph dict {title: [links]}
  → Iteratively expand by fetching links from discovered pages
  → Convert to NetworkX graph, check shortest_path()
  → Return path or "no path found"
```

### Key Files

| File | Purpose |
|------|---------|
| `front-end-implementation/wikiviz-app.py` | Streamlit web app (production) |
| `front-end-implementation/wikiviz-main.py` | CLI version for testing without Streamlit |
| `wikiviz.ipynb` | Main development/experimentation notebook |
| `scrap_wiki_scraper.ipynb` | Web scraping exploration notebook |

### Known Issues (from README)

- Graph direction is incorrect (A → B ← B instead of A → B)
- Network visualization not yet implemented
- Non-article links still pollute the graph
- API rate limiting on Streamlit Cloud deployment
- No user concurrency control
