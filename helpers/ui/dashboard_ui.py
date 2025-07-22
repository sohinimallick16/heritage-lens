# helpers/ui/dashboard_ui.py
import gradio as gr

def _make_dashboard_md(log_list):
    """Build one big markdown string from a list of entries."""
    if not log_list:
        return "No entries yet—generate something first!"
    md = []
    for i, e in enumerate(log_list, 1):
        md.append(f"# {i}. {e['site']} — {e['object']}  ⏱️ {e['time']}")
        md.append("#**Catalogue Entry**")
        md.append(e["catalogue_md"] or "_(none)_")
        if e.get("conservation_md"):
            md.append("**Conservation Assessment**")
            md.append(e["conservation_md"])
    return "\n\n".join(md)

def show_dashboard(log_state):
    with gr.Column():
        placeholder = gr.Markdown("No entries yet—generate something first!")
        # whenever log_state (a list) changes, re-run _make_dashboard_md
        log_state.change(
            fn=_make_dashboard_md,
            inputs=[log_state],
            outputs=[placeholder]
        )
# # helpers/ui/dashboard_ui.py
# import gradio as gr

# def show_dashboard(log_state):
#     gr.Markdown("## 📊 Heritage Dashboard")

#     # make an initial empty gallery with 4 columns and 150px height
#     gallery = gr.Gallery(
#         label="Click any entry to see full report",
#         columns=4,
#         height="150px",
#         elem_id="dash-gallery"
#     )

#     detail_img = gr.Image(label="Site image")
#     detail_md  = gr.Markdown()

#     # regenerate thumbnails any time log_state changes
#     def make_thumbnails(log_list):
#         return [ e["img_path"] for e in log_list ]

#     log_state.change(
#         fn=make_thumbnails,
#         inputs=[log_state],
#         outputs=[gallery],
#     )

#     # when the user clicks on a thumbnail, show full entry
#     def show_details(selected_path, log_list):
#         for entry in log_list:
#             if entry["img_path"] == selected_path:
#                 md = f"## {entry['site']} — {entry['object']}\n\n"
#                 md += entry["catalogue_md"] or ""
#                 if entry.get("conservation_md"):
#                     md += "\n\n---\n\n" + entry["conservation_md"]
#                 return selected_path, md
#         return None, "⚠️ Entry not found"

#     gallery.select(
#         fn=show_details,
#         inputs=[gallery, log_state],
#         outputs=[detail_img, detail_md]
#     )

