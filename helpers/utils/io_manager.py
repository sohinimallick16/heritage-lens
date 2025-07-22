# helpers/utils/io_manager.py
import tempfile, os
from pathlib import Path
from PIL import Image

class IOManager:
    @staticmethod
    def save_tmp(uploaded_file) -> str:
    # If Gradio already gave us a filepath, just return it
        if isinstance(uploaded_file, str) and os.path.isfile(uploaded_file):
            return uploaded_file

            # Otherwise assume it's a file‐like (with .name & .read())
        suffix = Path(uploaded_file.name).suffix
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(uploaded_file.read())
        tmp.flush()
        tmp.close()
        return tmp.name

    @staticmethod
    def load_image(path: str) -> Image.Image:
        """
        Open and return a PIL Image from disk.
        """
        return Image.open(path)
