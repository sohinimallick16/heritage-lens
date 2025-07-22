# app/utils/local_gemma.py

from .model import load_fast_gemma3n
from src.heritage_scribe.file_manager import FileManager
from transformers import TextStreamer
import torch
import gc

import time

timings = {}
# Load once per session
MODEL, PROCESSOR = load_fast_gemma3n()

def gemma3n_local_multimodal(
    image_path: str,
    prompt: str,
    temperature: float = 1.0,
    num_beams: int = 1,
    max_new_tokens: int = 1200,
    image_resolution: int | None = None
) -> str:
    
    # 1) Image load
    t0 = time.perf_counter()
    image = FileManager.load_image(image_path)
    timings["load_image"] = time.perf_counter() - t0

    # 2) Build messages
    messages = [
        {"role": "system", "content":[{"type":"text","text":"You are HeritageScribe, a digital assistant to archaeologists and heritage enthusiasts."}]},
        {"role": "user", "content": [
            {"type":"image","image":image},
            {"type":"text","text":prompt}
        ]}
    ]
    t0 = time.perf_counter()
    inputs = PROCESSOR.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
        return_dict=True
    ).to(MODEL.device)
    timings["tokenize"] = time.perf_counter() - t0

    # 3) Inference (Unsloth’s API is compatible with .generate)
    #torch.cuda.synchronize()
    t0 = time.perf_counter()
    prefix_len = inputs["input_ids"].shape[-1]
    #with torch.inference_mode():
    out_ids = MODEL.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            num_beams=num_beams,
            temperature=temperature,
            eos_token_id=MODEL.config.eos_token_id,
            use_cache =True,
            streamer=TextStreamer(PROCESSOR, skip_special_tokens=True)
        )[0][prefix_len:]
    timings["inference"] = time.perf_counter() - t0

    # 4) Decode
    t0 = time.perf_counter()
    result = PROCESSOR.decode(out_ids, skip_special_tokens=True)
    timings["decode"] = time.perf_counter() - t0

    # 5) Optional cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    gc.collect()
    
    # 6) Compute tokens/sec
    num_output_tokens = out_ids.shape[-1]
    timings["tokens_per_sec"] = num_output_tokens / timings["inference"]
    
    # 7) Log or print
    print({k: f"{v*1000:.1f} ms" if k!="tokens_per_sec" else f"{v:.1f} tok/s"
           for k,v in timings.items()})
    
    return result
