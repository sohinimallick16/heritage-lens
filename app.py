import gradio as gr
from helpers.ui.home_ui      import show_home
from helpers.ui.generate_ui  import show_generate
from helpers.ui.dashboard_ui import show_dashboard
from helpers.utils.log_state import LogState

def build_app():
    with gr.Blocks() as demo:
        log_state = gr.State([])

        gr.Markdown("# 🏺 HeritageScribe")

        tabs = gr.Tabs()
        with tabs:
            with gr.TabItem("🏠 Home"):
                show_home()
            with gr.TabItem("✍️ Generate"):
                show_generate(log_state)
            with gr.TabItem("📊 Dashboard"):
                show_dashboard(log_state)

    return demo

if __name__ == "__main__":
    build_app().launch()
