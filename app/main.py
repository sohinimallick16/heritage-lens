"# app/main.py"
import os,sys 
# 1) Compute project root
ROOT = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
# 2) Add root so `helpers` is on the path
sys.path.insert(0, ROOT)
# 3) Add src so `src.heritage_scribe` is on the path
sys.path.insert(0, os.path.join(ROOT, "src"))

import streamlit as st
from helpers.ui.home_ui      import show_home
from helpers.ui.generate_ui  import show_generate
from helpers.ui.dashboard_ui import show_dashboard

st.set_page_config(page_title="Heritage Lens", layout="wide")
tab_gen, tab_dash = st.tabs(["🛠️ Generate", "📊 Dashboard"])

with tab_gen:
    show_generate()

with tab_dash:
    show_dashboard()
