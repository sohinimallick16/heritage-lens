# helpers/ui/dashboard_ui.py
import streamlit as st
from src.display import render_markdown

def show_dashboard():
    st.header("📊 Heritage Dashboard")

    logs = st.session_state.get("catalogue_log", [])
    if not logs:
        st.info("No entries yet—generate something first!")
        return

    for idx, entry in enumerate(logs, start=1):
        st.subheader(f"{idx}. {entry['site']} — {entry['object']}")

        # show the uploaded image
        if entry.get("img_path"):
            st.image(entry["img_path"], use_container_width=True)

        # Catalogue
        st.markdown("**Catalogue Entry:**")
        render_markdown(entry["catalogue_md"])

        # Conservation
        if entry.get("conservation_md"):
            st.markdown("**Conservation Assessment:**")
            render_markdown(entry["conservation_md"])
