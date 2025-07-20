# src/heritage_scribe/app_utils.py
import time
import streamlit as st

def annotate_with_timing(scribe, **annotate_kwargs):
    """
    Call scribe.annotate(...) and measure elapsed seconds.
    Returns (md_str, elapsed_s).
    """
    start = time.time()
    md = scribe.annotate(**annotate_kwargs)
    return md, time.time() - start

def display_markdown(md: str):
    """
    Render the generated markdown in a nicer Streamlit card.
    """
    st.markdown(
        "<div style='background:#f9f9f9;padding:1rem;border-radius:8px;'>"
        + md.replace("\n", "<br>") +
        "</div>",
        unsafe_allow_html=True
    )
