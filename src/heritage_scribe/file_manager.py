# src/heritage_scribe/utils/file_manager.py
import os
from pathlib import Path
from PIL import Image

class FileManager:
    @staticmethod
    def read_base_template(template_path: str) -> str:
        if not os.path.isfile(template_path):
            raise FileNotFoundError(f"Base template missing: {template_path}")
        return Path(template_path).read_text(encoding="utf-8").strip()

    @staticmethod
    def read_user_prompt(txt_filename: str, data_dir: str) -> str:
        path = os.path.join(data_dir, txt_filename)
        if not path.lower().endswith(".txt") or not os.path.isfile(path):
            raise FileNotFoundError(f"Prompt file missing: {path}")
        return Path(path).read_text(encoding="utf-8").strip()

    @staticmethod
    def load_image(img_filename: str, data_dir: str) -> Image.Image:
        path = os.path.join(data_dir, img_filename)
        if not any(path.lower().endswith(ext) for ext in (".jpg",".png","jpeg")):
            raise FileNotFoundError(f"Image missing: {path}")
        return Image.open(path)
