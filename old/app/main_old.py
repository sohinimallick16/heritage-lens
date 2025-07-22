# app/main.py
import os, sys, time
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

import streamlit as st
import torch
from utils.local_gemma import gemma3n_local_multimodal
from src.heritage_scribe.prompt_manager import merge
from src.heritage_scribe.display import show_elapsed, render_markdown
from pathlib import Path
import tempfile

st.title("Heritage Lens")

# Sidebar device info
with st.sidebar:
    st.markdown("### System Info")
    st.markdown(f"**Device:** {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

    st.markdown("### Advanced Settings")
    num_beams = st.slider("Beam Search", 1, 5, 1)
    temperature = st.slider("Temperature", 0.1, 1.5, 1.0)
    max_tokens  = st.sidebar.slider("Max Output Tokens", 50, 1500, 800, 50)

    #image_resolution = st.sidebar.selectbox("Image Resize (px)", [None, 224, 384, 512], index=0)

# User Inputs
site_name = st.text_input("Site name (e.g. Ajanta Cave 10)", "")
site_location = st.text_input("Location (country,state,city)")
object_type = st.text_input("Object type (e.g. mural, relief)", "")
user_prompt   = st.text_area("Enter your prompt here", "")
img_file = st.file_uploader("Heritage image", type=["jpg", "png"])

if st.button("Generate catalogue entry"):
    if not (site_name and site_location and object_type and user_prompt and img_file):
        st.warning("Please complete all fields and upload an image files.")
    else:
        full_prompt = merge(site_name, object_type, user_prompt)

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(img_file.name).suffix) as tmp:
            tmp.write(img_file.read())
            tmp.flush()
            img_path = tmp.name

        start = time.time()
        with st.spinner("Analyzing image & generating entry…"):
            md = gemma3n_local_multimodal(
                    img_path,
                    full_prompt,
                    temperature=temperature,
                    num_beams=num_beams,
                    max_new_tokens=max_tokens,
                    #image_resolution=image_resolution
                )
        elapsed = time.time() - start
        st.success("Done!")

        show_elapsed(elapsed)
        render_markdown(md)
