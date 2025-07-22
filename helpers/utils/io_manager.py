# helpers/utils/io_manager.py
import tempfile
from pathlib import Path
from PIL import Image

class IOManager:
    @staticmethod
    def save_tmp(uploaded_file) -> str:
        """
        Save a Streamlit UploadFile to a temp file and return its path.
        """
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
