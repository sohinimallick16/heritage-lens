# helpers/ui/generate_ui.py
import time
import gradio as gr
from helpers.utils.io_manager     import IOManager
from helpers.utils.prompt_manager import PromptManager
from helpers.utils.gemma_manager  import load_gemma_manager

def _stream_and_log(
    image, site, loc, obj, note,
    temperature, num_beams, max_new_tokens,
    log_list
):
    # 1) save upload
    path = IOManager.save_tmp(image)
    # 2) build catalogue prompt
    prompt = PromptManager().build_catalogue(site, loc, obj, note)
    gm = load_gemma_manager()

    start = time.time()
    # 3) stream chunks
    for chunk in gm.stream_annotate(
        path, prompt,
        temperature=temperature,
        num_beams=num_beams,
        max_new_tokens=max_new_tokens
    ):
        yield chunk, log_list, ""  # blank status until done

    # 4) when done, append log + status
    elapsed = time.time() - start
    entry = {
        "site":            site,
        "object":          obj,
        "img_path":        path,
        "catalogue_md":    gm.last_md,
        "conservation_md": None,
        "time":            f"{elapsed:.1f}s"
    }
    new_log = log_list + [entry]
    yield gm.last_md, new_log, "✅ Done!"

def _stream_cons_and_log(
    image, site, loc, obj, note,
    temperature, num_beams, max_new_tokens,
    log_list
):
    # same pattern for conservation
    path   = IOManager.save_tmp(image)
    prompt = PromptManager().build_conservation(site, loc, obj, note)
    gm     = load_gemma_manager()

    start = time.time()
    for chunk in gm.stream_annotate(
        path, prompt,
        temperature=temperature,
        num_beams=num_beams,
        max_new_tokens=max_new_tokens
    ):
        yield chunk, log_list, ""

    elapsed = time.time() - start
    if log_list:
        updated = log_list.copy()
        updated[-1] = {
            **updated[-1],
            "conservation_md": gm.last_md,
            "time":            f"{elapsed:.1f}s"
        }
    else:
        updated = [{
            "site":            site,
            "object":          obj,
            "img_path":        path,
            "catalogue_md":    None,
            "conservation_md": gm.last_md,
            "time":            f"{elapsed:.1f}s"
        }]
    yield gm.last_md, updated, "✅ Done!"

def show_generate(log_state):
    pm = PromptManager()

    with gr.Row():
        # ─── Left: Inputs + preview ───────────────────────
        with gr.Column(scale=1):
            site    = gr.Textbox(label="Site Name")
            loc     = gr.Textbox(label="Location (country/state/city)")
            obj     = gr.Textbox(label="Object Type")
            note    = gr.Textbox(label="Custom Prompt", lines=3)
            image   = gr.Image(label="Heritage Image", type="filepath")
            image.change(lambda x: x, inputs=image)

            temperature    = gr.Slider(0.1, 1.5,   value=1.0, step=0.05, label="Temperature")
            num_beams      = gr.Slider(1,   5,     value=1,   step=1,    label="Beam Search")
            max_new_tokens = gr.Slider(50,  1500,  value=800, step=50,   label="Max Output Tokens")

        # ─── Right: Streaming + status ───────────────────
        with gr.Column(scale=1):
            tabs = gr.Tabs()

            # Catalogue tab
            with tabs:
                with gr.TabItem("📜 Catalogue"):
                    out_cat    = gr.Textbox(label="Catalogue Stream", lines=40)
                    status_cat = gr.Markdown("")
                    btn_cat    = gr.Button("Generate Catalogue")
                    btn_cat.click(
                        fn=_stream_and_log,
                        inputs=[image, site, loc, obj, note,
                                temperature, num_beams, max_new_tokens, log_state],
                        outputs=[out_cat, log_state, status_cat]
                    )

                # Conservation tab
                with gr.TabItem("🛡️ Conservation Assessment"):
                    out_cons     = gr.Textbox(label="Conservation Assessment Stream", lines=40)
                    status_cons  = gr.Markdown("")
                    btn_cons     = gr.Button("Generate Conservation Assessment Entry")
                    btn_cons.click(
                        fn=_stream_cons_and_log,
                        inputs=[image, site, loc, obj, note,
                                temperature, num_beams, max_new_tokens, log_state],
                        outputs=[out_cons, log_state, status_cons]
                    )
