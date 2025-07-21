# app/utils/model.py

import torch
from unsloth import FastModel
from transformers import AutoProcessor
import streamlit as st

MODEL_ID = "unsloth/gemma-3n-E2B-it"  # or any UnsloTh 4‑bit checkpoint

@st.cache_resource(show_spinner=False)
def load_fast_gemma3n():
    """
    Load Gemma3n via Unsloth’s FastModel API for 4‑bit inference.
    """
    model, tokenizer = FastModel.from_pretrained(
        model_name      = MODEL_ID,
        dtype           = None,      # auto FP16/BF16
        device_map      = "auto",     # auto device placement
        max_seq_length  = 2048,      # or whatever you need
        load_in_4bit    = True,      # 4‑bit weights
        full_finetuning = False,     # inference only
    )
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    return model.eval(), processor
