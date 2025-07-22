# helpers/utils/streamer.py
import threading
import torch
from transformers import TextIteratorStreamer

def stream_generate(
    model, processor, inputs, *,
    temperature, num_beams, max_new_tokens
):
    streamer = TextIteratorStreamer(
        processor.tokenizer, skip_special_tokens=True
    )
    # launch generation in background
    t = threading.Thread(
        target=model.generate,
        kwargs={
            **inputs,
            "temperature": temperature,
            "num_beams": num_beams,
            "max_new_tokens": max_new_tokens,
            "eos_token_id": model.config.eos_token_id,
            "streamer": streamer,
        },
        daemon=True
    )
    t.start()

    buf = ""
    for new_text in streamer:
        buf += new_text
        yield buf  # yield the growing buffer as each chunk arrives
    t.join()
