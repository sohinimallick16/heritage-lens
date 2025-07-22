# helpers/ui/home_ui.py
import gradio as gr

def show_home():
    gr.Markdown("## 🏛️ HeritageScribe")
    gr.Markdown(
        """
        Welcome to **HeritageScribe**—your AI companion for creating rich,
        factual catalogue entries of archaeological sites and artworks.

        Use the **Generate** tab to upload an image and get started!
        """.strip()
    )
