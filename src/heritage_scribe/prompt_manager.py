import os

# load at import time
_BASE_PATH = os.path.join(os.path.dirname(__file__), "templates", "base_prompt.txt")
with open(_BASE_PATH, "r", encoding="utf-8") as f:
    BASE_PROMPT = f.read()

def merge(site_type: str, object_type: str, user_prompt: str) -> str:
    """
    Fill in the base template and append the user’s custom prompt.
    """
    filled = BASE_PROMPT.format(site_type=site_type, object_type=object_type)
    return f"{filled}\n\n{user_prompt}"
