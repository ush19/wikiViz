"""Streamlit UI for wikiViz."""

from datetime import datetime

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

from wikiviz.core import find_shortest_path

st.set_page_config(page_title="wikiViz", page_icon=None, layout="wide")


def _wiki_url(title):
    """Convert a Wikipedia page title to a full URL."""
    return f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"


def _render_graph(path, graph):
    """Render the explored graph with the shortest path highlighted."""
    path_set = set(path)
    path_edges = set(zip(path, path[1:]))

    # Build nodes — only include nodes that appear in the graph keys
    # (i.e., pages we actually explored)
    nodes = []
    seen_nodes = set()
    for title in graph:
        if title in seen_nodes:
            continue
        seen_nodes.add(title)
        if title in path_set:
            nodes.append(Node(
                id=title,
                label=title,
                size=30,
                color="#1f77b4",
                font={"color": "#ffffff", "size": 14},
            ))
        else:
            nodes.append(Node(
                id=title,
                label=title,
                size=15,
                color="#cccccc",
                font={"color": "#666666", "size": 10},
            ))

    # Build edges — only between nodes we have in the graph
    edges = []
    for source, targets in graph.items():
        for target in targets:
            if target in seen_nodes:
                if (source, target) in path_edges:
                    edges.append(Edge(
                        source=source,
                        target=target,
                        color="#1f77b4",
                        width=3,
                    ))
                else:
                    edges.append(Edge(
                        source=source,
                        target=target,
                        color="#e0e0e0",
                        width=1,
                    ))

    config = Config(
        width=900,
        height=600,
        directed=True,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#ff4b4b",
    )

    agraph(nodes=nodes, edges=edges, config=config)


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
        status = st.empty()

        def on_progress(count, title):
            status.text(f"Exploring page {count}: {title}...")

        try:
            with st.spinner("Searching for a path..."):
                path, graph = find_shortest_path(
                    search_node_a, search_node_b, on_progress=on_progress
                )
            status.empty()
            degrees = len(path) - 1
            output = (
                f"There are {degrees} degrees of separation between "
                f"{path[0]} and {path[-1]}"
            )
            st.write(output)
            st.write("**Path:** " + " → ".join(path))
            for title in path:
                st.markdown(f"- [{title}]({_wiki_url(title)})")

            st.subheader("Network Graph")
            _render_graph(path, graph)

        except ValueError as e:
            status.empty()
            output = str(e)
            st.write(output)

        with open("app_run_logs.txt", "a") as log:
            log.write(f"{output}\n")
            log.write(f"Run: {now}\n\n")
