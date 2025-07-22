# src/heritage_scribe/display.py
import streamlit as st

_CSS = """
<style>
/* Container for the catalogue entry */
.catalogue-entry {
  background: #f9f9f9;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
  font-family: 'Segoe UI', sans-serif;
}

/* Headings */
.catalogue-entry h2 {
  margin-top: 0;
  color: #2c3e50;
  font-size: 1.5rem;
  border-bottom: 2px solid #ddd;
  padding-bottom: 0.25rem;
}

/* Lists */
.catalogue-entry ul {
  margin: 0.5rem 0 1rem 1.25rem;
}

/* Inline ticks */
.catalogue-entry input[type="checkbox"] {
  margin-right: 0.5rem;
}

/* Field‐log JSON in a monospace box */
.catalogue-entry pre.json-log {
  background: #ececec;
  padding: 0.75rem;
  border-radius: 0.25rem;
  overflow-x: auto;
}
</style>
"""

def show_elapsed(elapsed: float):
    st.sidebar.markdown(f"⏱️ Annotated in **{elapsed:.1f}s**")

def render_markdown(md: str):
    # inject CSS once
    st.markdown(_CSS, unsafe_allow_html=True)

    # wrap the whole markdown in a div.catalogue-entry so our CSS applies
    html = f'<div class="catalogue-entry">\n{md}\n</div>'
    st.markdown(html, unsafe_allow_html=True)
    
