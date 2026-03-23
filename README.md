# wikiViz

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Check out the [web app](https://wikiviz.streamlit.app/)!

Wikipedia degrees of separation calculator — finds the shortest path between any two Wikipedia pages.

## Inspiration

Inspiration for this project was drawn from [@terrence.png](https://www.tiktok.com/@terrence.png) on TikTok who maps two Wikipedia pages to each other with only the page's content and context. Combined with my interest in network science, I thought it'd be interesting to build a program to build the connections from nodes (Wikipedia pages) and the links which would lead from Wikipedia page A to Wikipedia page B.

## Installation

```bash
# Clone the repo
git clone https://github.com/ush19/wikiViz.git
cd wikiViz

# Install in development mode
pip install -e ".[dev]"
```

## Usage

### Web App (Streamlit)

```bash
streamlit run main.py
```

### Run Tests

```bash
pytest
```

## Project Structure

```
wikiviz/          # Python package
  core.py         # Core algorithm (get_links, clean_links, find_shortest_path)
  app.py          # Streamlit web UI
tests/            # pytest test suite
notebooks/        # Reference Jupyter notebooks
main.py           # Streamlit entry point
```

## How It Works

1. Fetches both Wikipedia pages via the Wikipedia-API
2. Extracts and cleans links from each page
3. Builds a directed graph with NetworkX
4. Iteratively expands the graph by fetching links from discovered pages
5. After each expansion, checks for a shortest path between the two pages
6. Returns the path or reports no connection found

## Future Work

- Fix direction of network graph (A → B instead of A → B ← B)
- Develop network visualization
- Reduce scope of links to only in-article links
- Implement additional NetworkX analysis functions

## Contact

- Email: palakurthisusheel@gmail.com
- [LinkedIn](https://www.linkedin.com/in/psusheel/)

## License

MIT License — see [LICENSE](LICENSE) for details.
