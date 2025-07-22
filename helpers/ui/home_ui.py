# helpers/ui/home_ui.py
import streamlit as st

def show_home():
    st.title("🏛️ Heritage Lens")
    st.markdown(
        """
        Welcome to Heritage Lens—your AI companion for creating rich,
        factual catalogue entries of archaeological sites and artworks.
        Use the “Generate” tab to upload an image and get started!
        """,
        unsafe_allow_html=True
    )
