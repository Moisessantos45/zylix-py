import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(sys.executable).parent))

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal

from .styles import SIDEBAR_STYLE, VERDE_OSCURO, VERDE_MANZANA, VERDE_CLARO


class Sidebar(QWidget):

    operation_selected = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(SIDEBAR_STYLE)
        self._current_category = None
        self._buttons = {}
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        title = QLabel("Herramientas")
        title.setStyleSheet(f"color: white; font-size: 18px; font-weight: bold; padding: 15px;")
        layout.addWidget(title)

        self._add_category("PDF", [
            ("pdf_to_image", "PDF a Imagen"),
            ("image_to_pdf", "Imagen a PDF"),
            ("merge_pdfs", "Unir PDFs"),
            ("split_pdf", "Dividir PDF"),
            ("compress_pdf", "Comprimir PDF"),
            ("extract_text_pdf", "Extraer Texto"),
            ("add_watermark", "Marca de Agua"),
            ("rotate_pdf", "Rotar PDF"),
        ])

        self._add_category("Imagen", [
            ("convert_format", "Cambiar Formato"),
            ("optimize_image", "Optimizar"),
            ("rotate_image", "Rotar"),
            ("remove_background", "Remover Fondo"),
            ("ocr_image", "OCR de Imagen"),
            ("image_to_word", "Imagen a Word"),
        ])

        layout.addStretch()

    def _add_category(self, name: str, operations: list):
        header = QLabel(name)
        header.setStyleSheet("""
            color: white;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
            padding: 10px 15px 5px;
            background-color: #558B2F;
        """)
        self.layout().addWidget(header)

        for op_id, op_name in operations:
            btn = QPushButton(f"  {op_name}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    text-align: left;
                    font-size: 13px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.15);
                }
            """)
            btn.clicked.connect(lambda checked, c=name, o=op_id: self._select_operation(c, o))
            self.layout().addWidget(btn)
            self._buttons[op_id] = btn

    def _select_operation(self, category: str, operation_id: str):
        if self._current_category:
            for btn in self._buttons.values():
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: white;
                        border: none;
                        padding: 8px 15px;
                        text-align: left;
                        font-size: 13px;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255,255,255,0.15);
                    }
                """)

        btn = self._buttons.get(operation_id)
        if btn:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.25);
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    text-align: left;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 4px;
                }
            """)

        self._current_category = operation_id
        self.operation_selected.emit(category, operation_id)
