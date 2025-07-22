# src/heritage_scribe/utils/file_manager.py
import os
import tempfile    
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
    def load_image(path_or_filename: str, data_dir: str = None) -> Image.Image:
        """
        Load from a full path if it exists; otherwise, load from data_dir/filename.
        """
        # if it's already an absolute or relative path on disk:
        if os.path.isfile(path_or_filename):
            return Image.open(path_or_filename)

        # fallback: interpret as filename inside data_dir
        if data_dir is None:
            raise FileNotFoundError(f"Image not found: {path_or_filename}")

        full_path = os.path.join(data_dir, path_or_filename)
        if not any(full_path.lower().endswith(ext) for ext in (".jpg", ".png", ".jpeg")):
            raise FileNotFoundError(f"Image missing: {full_path}")
        return Image.open(full_path)

    @staticmethod
    def save_temp(uploaded_file) -> str:
        suffix = Path(uploaded_file.name).suffix
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(uploaded_file.read())  
        tmp.flush()
        tmp.close()
        return tmp.name