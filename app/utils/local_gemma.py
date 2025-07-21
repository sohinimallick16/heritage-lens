# app/utils/local_gemma.py

from .model_loader import load_fast_gemma3n
from src.heritage_scribe.file_manager import FileManager
import torch
import gc

# Load once per session
MODEL, PROCESSOR = load_fast_gemma3n()

def gemma3n_local_multimodal(
    image_path: str,
    prompt: str,
    temperature: float = 1.0,
    num_beams: int = 1,
    max_new_tokens: int = 100,
    image_resolution: int | None = None
) -> str:
    # 1) Load image bytes
    image = FileManager.load_image(image_path)

    # 2) Build messages
    messages = [
        {"role": "system", "content":[{"type":"text","text":"You are HeritageScribe."}]},
        {"role": "user", "content": [
            {"type":"image","image":image},
            {"type":"text","text":prompt}
        ]}
    ]
    inputs = PROCESSOR.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
        return_dict=True
    ).to(MODEL.device)

    # 3) Inference (Unsloth’s API is compatible with .generate)
    prefix_len = inputs["input_ids"].shape[-1]
    with torch.inference_mode():
        out_ids = MODEL.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            num_beams=num_beams,
            temperature=temperature,
            eos_token_id=MODEL.config.eos_token_id,
            use_cache =True,
        )[0][prefix_len:]

    # 4) Decode
    result = PROCESSOR.decode(out_ids, skip_special_tokens=True)

    # 5) Optional cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    gc.collect()
    
    return result
