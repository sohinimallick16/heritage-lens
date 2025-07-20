# heritage_scribe/core.py
import torch
from .file_manager import FileManager

class HeritageScribe:
    def __init__(self, model, processor):
        self.model     = model
        self.processor = processor

    def annotate(self, img_path, prompt_text: str, **gen_kwargs) -> str:
        image = FileManager.load_image(img_path)
        messages = [
          {"role":"system",  "content":[{"type":"text","text":"You are HeritageScribe."}]},
          {"role":"user",    "content":[{"type":"image","image":image},
                                         {"type":"text","text":prompt_text}]},
        ]
        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.model.device)
        prefix_len = inputs["input_ids"].shape[-1]
        with torch.inference_mode():
            out = self.model.generate(**inputs, **gen_kwargs)[0][prefix_len:]
        return self.processor.decode(out, skip_special_tokens=True)
