# helpers/utils/gemma_manager.py
import torch, gc, threading
from unsloth import FastModel
from transformers import AutoProcessor, TextIteratorStreamer
import streamlit as st
import re
from helpers.utils.io_manager import IOManager
torch._dynamo.config.cache_size_limit = 40_000
torch._dynamo.config.recompile_limit  = 1_000

MODEL_ID = "unsloth/gemma-3n-E2B-it"
# Factory function to cache the loaded model+processor
@st.cache_resource(show_spinner=False)
def load_gemma_manager():
    """ Load the Gemma model and processor, caching the result.
    This function is decorated with @st.cache_resource to ensure that the model
    and processor are loaded only once and reused across Streamlit runs.
    """
    # FastModel handles the 4‑bit quantization load
    model, _ = FastModel.from_pretrained(
        model_name=MODEL_ID,
        load_in_4bit=True,
        max_seq_length=2048, 
        full_finetuning=False
    )
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    return GemmaManager(model, processor)

class GemmaManager:
    def __init__(self, model, processor):
        self.model     = model
        self.processor = processor
        self.model.eval()
    
    def stream_annotate(
        self,
        image_path: str,
        prompt: str,
        *,
        temperature: float = 1.5,
        num_beams: int      = 1.0,
        max_new_tokens: int = 800
    ):
        image = IOManager.load_image(image_path)
        messages = [
            {"role":"system","content":[{"type":"text","text":"You are HeritageScribe."}]},
            {"role":"user","content":[
                {"type":"image","image": image},
                {"type":"text","text": prompt}
            ]},
        ]

        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_tensors="pt",
            return_dict=True
        ).to(self.model.device)

        streamer = TextIteratorStreamer(
            self.processor.tokenizer, skip_special_tokens=True
        )
        threading.Thread(
            target=self.model.generate,
            kwargs={
                **inputs,
                "temperature":    temperature,
                "num_beams":      num_beams,
                "max_new_tokens": max_new_tokens,
                "eos_token_id":   self.model.config.eos_token_id,
                "streamer":       streamer,
                "use_cache":      True,
            },
            daemon=True
        ).start()

        #marker = re.escape("<<<INFERENCE_START>>>")
        marker = "model"
        buffer = ""
        started = False
        # compile a regex for your marker
        
        #pattern    = re.compile(marker_pat)

        for chunk in streamer:
            buffer += chunk

            if not started:
                idx = buffer.find(marker)
                if idx < 0:
                    # still in the prompt‑echo region
                    continue
                # drop everything up through the marker
                buffer = buffer[idx + len(marker):]
                started = True

            # 5) now yield each time new text arrives
            yield buffer

        # 6) stash full MD
        self.last_md = buffer

        # cleanup…
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        gc.collect()

    def annotate(  # synchronous wrapper, if you ever want it
        self, image_path, prompt, **gen_kwargs
    ) -> str:
        for _ in self.stream_annotate(image_path, prompt, **gen_kwargs):
            pass
        return self.last_md

