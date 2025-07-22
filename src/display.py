import streamlit as st

_CSS = """
<style>
.catalogue-entry {
  background: #f9f9f9;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
  font-family: 'Segoe UI', sans-serif;
}
.catalogue-entry h2 {
  margin-top: 0;
  color: #2c3e50;
  font-size: 1.5rem;
  border-bottom: 2px solid #ddd;
  padding-bottom: 0.25rem;
}
.catalogue-entry ul {
  margin: 0.5rem 0 1rem 1.25rem;
}
.catalogue-entry input[type="checkbox"] {
  margin-right: 0.5rem;
}
.catalogue-entry pre.json-log {
  background: #ececec;
  padding: 0.75rem;
  border-radius: 0.25rem;
  overflow-x: auto;
}
</style>
"""

def show_elapsed(elapsed: float):
    """Sidebar timing display."""
    st.sidebar.markdown(f"⏱️ Annotated in **{elapsed:.1f}s**")

def render_markdown(md: str):
    """Wrap generated markdown in a styled div."""
    st.markdown(_CSS, unsafe_allow_html=True)
    html = f'<div class="catalogue-entry">\n{md}\n</div>'
    st.markdown(html, unsafe_allow_html=True)
