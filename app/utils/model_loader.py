# app/utils/model.py
from unsloth import FastLanguageModel
import torch
from transformers import (
    AutoConfig,
    AutoProcessor,
    Gemma3nForConditionalGeneration,
)
import streamlit as st

MODEL_ID = "google/gemma-3n-e4b-it"

@st.cache_resource(show_spinner=False)
def load_fast_gemma3n():
    """
    Load Gemma3n in FP16/BF16, optionally torch.compile it,
    then wrap with Unsloth for fast inference.
    """
    # 1) Base config
    config = AutoConfig.from_pretrained(MODEL_ID)
    config.load_audio  = False
    config.load_vision = True

    # 2) Choose mixed precision if available
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    torch.backends.cuda.matmul.allow_tf32 = True

    # 3) Load full‑precision / mixed‑precision model
    model = Gemma3nForConditionalGeneration.from_pretrained(
        MODEL_ID,
        config=config,
        torch_dtype=dtype,
        device_map="cpu",
        low_cpu_mem_usage=True,
    )

    # 4) Optional compile for PyTorch 2.0+
    #if hasattr(torch, "compile"):
    #    try:
    #        model = torch.compile(model, mode="reduce-overhead")
    #    except Exception:
    #        pass

    # 5) Wrap with Unsloth for optimized kernels
    fast_model = FastLanguageModel.for_inference(model)

    # 6) Load processor
    processor = AutoProcessor.from_pretrained(MODEL_ID)

    return fast_model.eval(), processor
