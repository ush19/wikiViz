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
