# app/utils/model.py
"""Utility functions to load the Gemma3n model with 4-bit quantization
using UnsloTh's FastModel API for efficient inference in Streamlit."""

import torch

#  Allow more graphs if you still want some dynamic recompiles
torch._dynamo.config.cache_size_limit = 20_000
torch._dynamo.config.recompile_limit  = 1_000

from unsloth import FastModel
from transformers import AutoProcessor
import streamlit as st

# Use the UnsloTh 4-bit quantized checkpoint for fast inference
#MODEL_ID = "unsloth/gemma-3n-E4B-it-unsloth-bnb-4bit"
MODEL_ID = "unsloth/gemma-3n-E2B-it"
@st.cache_resource(show_spinner=False)
def load_fast_gemma3n():
    """
    Load the Gemma3n model in 4-bit via Unsloth's FastModel API for optimized inference.
    """
    # Auto-detect FP16/BF16 for best performance
    dtype = None  # Unsloth will auto-select based on hardware capabilities

    # Load model + tokenizer with 4-bit quantization and offloading
    model, tokenizer = FastModel.from_pretrained(
        model_name=MODEL_ID,
        dtype=dtype,
       max_seq_length=2048,          # supports up to 2048 tokens context
        load_in_4bit=True,
        full_finetuning=False        # inference-only mode
    )

    # Load processor (handles vision+text for Gemma3n)
    processor = AutoProcessor.from_pretrained(MODEL_ID)

    # Return model.eval() for inference and processor
    return model.eval(), processor
