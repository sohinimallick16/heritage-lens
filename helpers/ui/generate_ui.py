import streamlit as st
import time 
from helpers.utils.io_manager      import IOManager
from helpers.utils.prompt_manager  import PromptManager
from helpers.utils.gemma_manager import load_gemma_manager
#from helpers.utils.streamer       import stream_generate
from src.display   import render_markdown, show_elapsed

def show_generate():
    st.header("Generate Heritage Entry")

    # common inputs
    site = st.text_input("Site name")
    loc  = st.text_input("Location (country/state/city)")
    obj  = st.text_input("Object type")
    note = st.text_area("Custom prompt")
    img  = st.file_uploader("Heritage image", type=["jpg","png"])

    gm = load_gemma_manager()
    pm   = PromptManager()

    tab_cat, tab_cons = st.tabs(["📜 Catalogue", "🛡️ Conservation"])

    with tab_cat:
        st.subheader("Heritage Catalogue")
        if st.button("Generate Catalogue", key="gen_cat") and all([site,loc,obj,note,img]):
            
            path = IOManager.save_tmp(img)
            prompt = pm.build_catalogue(site, loc, obj, note)
            placeholder = st.empty()
            start = time.time()
            with st.spinner("Generating catalogue…"):
                #st.write("→ gm.annotate() now") 
                for partial in gm.stream_annotate(path, prompt):
                    placeholder.text(partial)
            elapsed = time.time() - start
            st.success("Catalogue generated!")
            show_elapsed(elapsed)
            
            st.session_state.setdefault("catalogue_log", []).append({
                "site":         site,
                "object":       obj,
                "img_path":      path,
                "catalogue_md": gm.last_md,
            })

    with tab_cons:
        st.subheader("Conservation Assessment")
        if st.button("Generate Conservation Assessment", key="gen_cons") and all([site,loc,obj,note,img]):
            
            path = IOManager.save_tmp(img)
            prompt = pm.build_conservation(site, loc, obj, note)
            placeholder = st.empty()
            start = time.time()
            with st.spinner("Generating conservation assessment…"):
                for partial in gm.stream_annotate(path, prompt):
                    placeholder.text(partial)
            elapsed = time.time() - start
            st.success("Conservation assesment done!")
            show_elapsed(elapsed)
            st.session_state["catalogue_log"][-1].update({
                "conservation_md": gm.last_md
            })

