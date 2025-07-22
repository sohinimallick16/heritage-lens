import streamlit as st
from pathlib import Path
import sys, os

# ensure we can import our app/utils and src packages
sys.path.append(os.path.abspath(os.path.join(__file__,"..")))

from utils.home_ui       import show_home
from utils.generate_ui   import show_generate
from utils.dashboard_ui  import show_dashboard

st.set_page_config(page_title="Heritage Lens", layout="wide")
page = st.sidebar.radio("Go to", ["Home","Generate","Dashboard"])

if page == "Home":
    show_home()
elif page == "Generate":
    show_generate()
elif page == "Dashboard":
    show_dashboard()