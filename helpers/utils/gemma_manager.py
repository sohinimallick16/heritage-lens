# helpers/utils/gemma_manager.py
import spaces
from functools import lru_cache
import torch, gc, threading
from unsloth import FastModel
from transformers import AutoProcessor, TextIteratorStreamer
from helpers.utils.io_manager import IOManager

torch._dynamo.config.cache_size_limit = 40_000
torch._dynamo.config.recompile_limit  = 1_000

# --- your model checkpoint ---
MODEL_ID = "unsloth/gemma-3n-E2B-it"

@spaces.GPU  # ZeroGPU will allocate/release an NVIDIA H200 for this function
#@lru_cache(maxsize=1)
def load_gemma_manager():
    """
    Load the Gemma model and processor, returning a GemmaManager.
    ZeroGPU will spin up a GPU only while this is running.
    """
    # FastModel handles the 4‑bit quantized load
    model, _ = FastModel.from_pretrained(
        model_name=MODEL_ID,
        load_in_4bit=True,
        max_seq_length=2048,
        full_finetuning=False,
    )
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    return GemmaManager(model.eval(), processor)


class GemmaManager:
    """
    Wrapper for Gemma that supports streaming markdown output
    and strips out the prompt‑echo up to a user‑defined marker.
    """

    def __init__(self, model, processor):
        self.model     = model
        self.processor = processor
        self.last_md   = ""

    @spaces.GPU(timeout=300)  # decorate inference to get a GPU slice during generation
    def stream_annotate(
        self,
        image_path: str,
        prompt: str,
        *,
        temperature: float = 1.5,
        num_beams: int      = 1,
        max_new_tokens: int = 800,
    ):
        """
        Streams chunks of generated markdown, skipping the initial prompt echo.
        Yields:
            str: the cumulative markdown generated so far (after the marker).
        """
        # 1) load the image
        image = IOManager.load_image(image_path)

        # 2) build chat messages
        messages = [
            {"role":"system", "content":[{"type":"text","text":"You are HeritageScribe."}]},
            {"role":"user",   "content":[
                {"type":"image","image": image},
                {"type":"text","text": prompt}
            ]},
        ]

        # 3) tokenize once
        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_tensors="pt",
            return_dict=True,
        ).to(self.model.device)

        # 4) set up a streamer
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
            daemon=True,
        ).start()

        # 5) skip prompt‑echo until we see our marker
        marker = "model"  # choose a unique sentinel
        buffer  = ""
        started = False

        for chunk in streamer:
            buffer += chunk
            if not started:
                idx = buffer.find(marker)
                if idx < 0:
                    continue
                # drop everything through the marker
                buffer  = buffer[idx + len(marker):]
                started = True

            # yield the cleaned buffer each time new text arrives
            yield buffer

        # 6) store full markdown
        self.last_md = buffer

        # 7) cleanup
        #if torch.cuda.is_available():
            #torch.cuda.empty_cache()
            #torch.cuda.ipc_collect()
        #gc.collect()

    def annotate(self, image_path: str, prompt: str, **gen_kwargs) -> str:
        """
        Blocking wrapper: runs through the streamer to completion
        and returns the full markdown.
        """
        for _ in self.stream_annotate(image_path, prompt, **gen_kwargs):
            pass
        return self.last_md
