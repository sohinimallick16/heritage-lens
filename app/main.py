# app/main.py
import os, time, torch
# add the parent directory to the path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    

import streamlit as st
from heritage_scribe.file_manager   import FileManager
from heritage_scribe.prompt_manager import merge
from heritage_scribe.core          import HeritageScribe
from heritage_scribe.display       import show_elapsed, render_markdown
from app.utils.model_loader        import load_scribe  

st.title("Heritage Lens")

# 1) Upload / parameters
site_name   = st.text_input("Site name (e.g. Ajanta Cave 10)", "")
object_type = st.text_input("Object type (e.g. mural, relief, archaeological site", "")
user_file   = st.file_uploader("Your custom prompt (.txt)", type="txt")
img_file    = st.file_uploader("Heritage image", type=["jpg","png"])

if st.button("Generate catalogue entry") and site_name and user_file and img_file:
    # read the small user prompt
    user_prompt = user_file.read().decode("utf-8")
    # merge with a hard‑coded base template
    full_prompt = merge(site_name, object_type, user_prompt)

    # 2) load model (cached by Streamlit)
    model, processor = load_scribe(
        os.getenv("MODEL_DIR", "models/gemma-3n"),
        "cuda" if torch.cuda.is_available() else "cpu",
    )
    scribe = HeritageScribe(model, processor)

    # 3) run & time
    start = time.time()
    md    = scribe.annotate(
        img_path               = FileManager.save_temp(img_file),
        prompt_text            = full_prompt,
        max_new_tokens         = 500,
        do_sample              = False,
        temperature            = 0.9,
        top_p                  = 0.99,
        repetition_penalty     = 1.2,
        no_repeat_ngram_size   = 3,
        eos_token_id           = model.config.pad_token_id,
    )
    elapsed = time.time() - start

    # 4) display
    show_elapsed(elapsed)
    render_markdown(md)