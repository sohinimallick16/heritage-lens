# helpers/utils/display.py

def show_elapsed(elapsed: float) -> str:
    """
    Returns a small italicized string for display in a gr.Markdown box,
    indicating how long the generation took.
    """
    return f"*⏱️ Annotated in {elapsed:.1f}s*"


def render_markdown(md: str) -> str:
    """
    Just pass the raw markdown through so Gradio can render it with its
    default theme. If you want a container-style effect, you can wrap
    it in a blockquote or headings.
    """
    # For example, wrap in a blockquote to give it a slight inset look:
    # return "\n".join(["> " + line for line in md.splitlines()])
    return md
