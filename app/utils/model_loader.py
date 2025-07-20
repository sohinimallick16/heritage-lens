# app/utils/model_loader.py
import torch, os, streamlit as st
from transformers import AutoModelForCausalLM, AutoProcessor

@st.cache_resource(show_spinner=False)
def load_scribe(device: str):
    """
    Load (and cache) the HeritageScribe backbone model + processor.
    """
    model_dir = os.path.expanduser("~/models/gemma-3n-e4b-it")
    # replace with whichever model class you actually use:
    model = AutoModelForCausalLM.from_pretrained(model_dir).to(device).eval()
    processor = AutoProcessor.from_pretrained(model_dir)
    return model, processor
