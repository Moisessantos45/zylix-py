from pathlib import Path
from PIL import Image
import pytesseract


class OCREngine:

    def __init__(self):
        self._available = self._check_tesseract()

    def _check_tesseract(self) -> bool:
        try:
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False

    @property
    def is_available(self) -> bool:
        return self._available

    def extract_text(self, image_path: Path, lang: str = "eng") -> str:

        if not self._available:
            return "Error: Tesseract OCR no está disponible. Asegúrate de tener tesseract instalado."

        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang=lang)
            return text.strip()
        except Exception as e:
            return f"Error en OCR: {str(e)}"

    def extract_text_with_boxes(self, image_path: Path, lang: str = "eng"):
        if not self._available:
            return None

        img = Image.open(image_path)
        data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
        return data
