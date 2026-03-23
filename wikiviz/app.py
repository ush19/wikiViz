"""Streamlit UI for wikiViz."""

from datetime import datetime

import streamlit as st

from wikiviz.core import find_shortest_path

st.set_page_config(page_title="wikiViz", page_icon=None, layout="centered")


def _wiki_url(title):
    """Convert a Wikipedia page title to a full URL."""
    return f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"


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
                path = find_shortest_path(
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
        except ValueError as e:
            status.empty()
            output = str(e)
            st.write(output)

        with open("app_run_logs.txt", "a") as log:
            log.write(f"{output}\n")
            log.write(f"Run: {now}\n\n")
