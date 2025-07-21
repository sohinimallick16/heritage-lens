# src/heritage_scribe/prompt_manager.py
from pathlib import Path

# load once at import
BASE_PROMPT = Path(__file__).resolve().parents[2] / "templates" / "base_prompt.txt"
BASE_PROMPT = BASE_PROMPT.read_text(encoding="utf-8")

def merge(site_name: str, object_type: str, user_prompt: str) -> str:
    """
    Substitute only the two fields you collect from the user,
    leaving the rest for the model to fill.
    """
    filled = BASE_PROMPT.replace("{site_name}", site_name)\
                        .replace("{object_type}", object_type)
    return f"{filled}\n\n{user_prompt}"
