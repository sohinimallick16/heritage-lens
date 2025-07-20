import streamlit as st
import time

def show_elapsed(start: float, end: float):
    st.sidebar.markdown(f"⏱️ Annotated in **{end-start:.1f}s**")

def render_markdown(md: str):
    # you can tweak CSS or use st.markdown(…, unsafe_allow_html=True)
    st.markdown(md, unsafe_allow_html=True)