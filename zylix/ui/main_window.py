import sys
import os
from pathlib import Path

# Fix imports for PyInstaller
if getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(sys.executable).parent))

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QComboBox, QSlider, QGroupBox,
    QTextEdit, QScrollArea, QProgressBar, QMessageBox, QLineEdit, QCheckBox
)
from PySide6.QtCore import Qt, QThread, Signal

from .sidebar import Sidebar
from .file_selector import FileSelector
from .styles import MAIN_STYLE, VERDE_MANZANA, VERDE_CLARO

from ..core.base import OperationBase
from ..core.pdf_operations import (
    PdfToImage, MergePdfs, SplitPdf,
    CompressPdf, ExtractTextFromPdf, AddWatermark, RotatePdf
)
from ..core.image_operations import (
    ImageToPdf, ImageToWord, ConvertImageFormat, OptimizeImage, RotateImage,
    RemoveBackground, ExtractTextFromImage
)
from ..utils.file_manager import FileManager


OPERATIONS = {
    "pdf_to_image": PdfToImage(),
    "image_to_pdf": ImageToPdf(),
    "merge_pdfs": MergePdfs(),
    "split_pdf": SplitPdf(),
    "compress_pdf": CompressPdf(),
    "extract_text_pdf": ExtractTextFromPdf(),
    "add_watermark": AddWatermark(),
    "rotate_pdf": RotatePdf(),
    "convert_format": ConvertImageFormat(),
    "optimize_image": OptimizeImage(),
    "rotate_image": RotateImage(),
    "remove_background": RemoveBackground(),
    "ocr_image": ExtractTextFromImage(),
    "image_to_word": ImageToWord(),
}


class Worker(QThread):
    finished = Signal(bool, str)
    progress = Signal(int, str)

    def __init__(self, operation: OperationBase, input_files: list, output_dir: Path, params: dict):
        super().__init__()
        self.operation = operation
        self.input_files = input_files
        self.output_dir = output_dir
        self.params = params

    def run(self):
        try:
            result = self.operation.execute(self.input_files, self.output_dir, **self.params)
            self.finished.emit(result.success, result.message)
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zylix - Manipulación de Archivos")
        self.setMinimumSize(1000, 700)
        self._current_operation = None
        self._worker = None
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        central.setObjectName("central_widget")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        self.sidebar = Sidebar()
        self.sidebar.operation_selected.connect(self._on_operation_selected)
        self.sidebar.setFixedWidth(200)
        main_layout.addWidget(self.sidebar)

        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_area.setWidget(self.content_widget)
        main_layout.addWidget(self.content_area, 1)

        self._show_welcome()

    def _show_welcome(self):
        self._clear_content()
        welcome = QLabel("Bienvenido a Zylix\n\nSelecciona una herramienta del menú lateral para comenzar.")
        welcome.setStyleSheet("color: #689F38; font-size: 18px; padding: 50px; text-align: center;")
        welcome.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(welcome)

    def _clear_content(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _on_operation_selected(self, category: str, operation_id: str):
        self._current_operation = operation_id
        self._show_operation_ui(operation_id)

    def _show_operation_ui(self, operation_id: str):
        self._clear_content()

        operation = OPERATIONS.get(operation_id)
        if not operation:
            return

        title = QLabel(operation.name)
        title.setStyleSheet("color: #33691E; font-size: 24px; font-weight: bold; padding: 10px 0;")
        self.content_layout.addWidget(title)

        desc = QLabel(f"Categoría: {operation.category.upper()}")
        desc.setStyleSheet("color: #558B2F; font-size: 13px; padding-bottom: 15px;")
        self.content_layout.addWidget(desc)

        self.file_selector = FileSelector()
        self.file_selector.set_extensions(operation.input_extensions)
        self.content_layout.addWidget(self.file_selector)

        options_group = QGroupBox("Opciones")
        options_layout = QVBoxLayout()

        self._add_operation_options(operation_id, options_layout)
        options_group.setLayout(options_layout)
        self.content_layout.addWidget(options_group)

        self.process_btn = QPushButton("Procesar")
        self.process_btn.setObjectName("process_btn")
        self.process_btn.setMinimumHeight(45)
        self.process_btn.clicked.connect(self._process)
        self.content_layout.addWidget(self.process_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.content_layout.addWidget(self.progress_bar)

        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        self.status_text.setPlaceholderText("Estado de la operación...")
        self.content_layout.addWidget(self.status_text)

        self.content_layout.addStretch()

    def _add_operation_options(self, operation_id: str, layout):
        if operation_id == "pdf_to_image":
            self._add_combobox(layout, "Formato:", "format", ["png", "jpg", "webp"])
            self._add_slider(layout, "DPI:", "dpi", 72, 600, 300)

        elif operation_id == "image_to_pdf":
            self._add_combobox(layout, "Modo:", "mode", ["separado", "unido"])
            self._add_text_input(layout, "Nombre de salida:", "output_name")

        elif operation_id == "merge_pdfs":
            self._add_text_input(layout, "Nombre de salida:", "output_name")

        elif operation_id == "compress_pdf":
            self._add_combobox(layout, "Calidad:", "quality", ["low", "medium", "high"])
            self._add_text_input(layout, "Nombre de salida:", "output_name")

        elif operation_id == "rotate_pdf":
            self._add_combobox(layout, "Ángulo:", "angle", ["0", "90", "180", "270"])
            self._add_text_input(layout, "Nombre de salida:", "output_name")

        elif operation_id == "optimize_image":
            self._add_slider(layout, "Calidad (1-100):", "quality", 1, 100, 85)

        elif operation_id == "convert_format":
            self._add_combobox(layout, "Formato:", "format", ["png", "jpg", "webp", "bmp"])

        elif operation_id == "rotate_image":
            self._add_combobox(layout, "Ángulo:", "angle", ["0", "90", "180", "270"])

        elif operation_id == "add_watermark":
            self._add_text_input(layout, "Texto:", "text")
            self._add_text_input(layout, "Nombre de salida:", "output_name")

        elif operation_id == "image_to_word":
            self._add_checkbox(layout, "Agregar página en blanco al inicio", "add_blank_page")
            self._add_text_input(layout, "Nombre de salida:", "output_name")

    def _add_combobox(self, layout, label: str, param_name: str, options: list):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        combo = QComboBox()
        combo.addItems(options)
        combo.setObjectName(param_name)
        row.addWidget(combo)
        layout.addLayout(row)

    def _update_process_button(self):
        pass

    def _add_slider(self, layout, label: str, param_name: str, min_val: int, max_val: int, default: int):
        row = QVBoxLayout()
        row.addWidget(QLabel(label))
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default)
        slider.setObjectName(param_name)
        value_label = QLabel(str(default))
        value_label.setObjectName(f"{param_name}_value")
        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))
        row.addWidget(slider)
        row.addWidget(value_label)
        layout.addLayout(row)

    def _add_text_input(self, layout, label: str, param_name: str):
        from PySide6.QtWidgets import QLineEdit
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        line_edit = QLineEdit()
        line_edit.setObjectName(param_name)
        row.addWidget(line_edit)
        layout.addLayout(row)

    def _add_checkbox(self, layout, label: str, param_name: str):
        from PySide6.QtWidgets import QCheckBox
        row = QHBoxLayout()
        checkbox = QCheckBox(label)
        checkbox.setObjectName(param_name)
        row.addWidget(checkbox)
        layout.addLayout(row)

    def _get_operation_params(self, operation_id: str) -> dict:
        params = {}
        item = self.content_layout.itemAt(3)
        options_group = item.widget() if item else None

        if options_group and hasattr(options_group, 'layout'):
            for i in range(options_group.layout().count()):
                item = options_group.layout().itemAt(i)
                if item.layout():
                    for j in range(item.layout().count()):
                        widget = item.layout().itemAt(j).widget()
                        if widget and hasattr(widget, 'objectName'):
                            name = widget.objectName()
                            if name == "format":
                                params['format'] = widget.currentText()
                            elif name == "quality" and isinstance(widget, QComboBox):
                                params['quality'] = widget.currentText()
                            elif name == "angle" and isinstance(widget, QSlider):
                                params['angle'] = widget.value()
                            elif name == "angle" and isinstance(widget, QComboBox):
                                params['angle'] = int(widget.currentText())
                            elif name == "dpi" and isinstance(widget, QSlider):
                                params['dpi'] = widget.value()
                            elif name == "text" and isinstance(widget, QLineEdit):
                                params['text'] = widget.text()
                            elif name == "mode":
                                params['mode'] = "joined" if widget.currentIndex() == 1 else "separate"
                            elif name == "output_name" and isinstance(widget, QLineEdit):
                                params['output_name'] = widget.text()
                            elif name == "add_blank_page" and isinstance(widget, QCheckBox):
                                params['add_blank_page'] = widget.isChecked()

        return params

    def _process(self):
        if not self._current_operation:
            return

        operation = OPERATIONS.get(self._current_operation)
        if not operation:
            return

        input_files = self.file_selector.get_selected_files()
        if not input_files:
            QMessageBox.warning(self, "Sin archivos", "Por favor selecciona al menos un archivo.")
            return

        if not self.file_selector.has_output_dir():
            QMessageBox.warning(self, "Sin ruta de salida", "Por favor selecciona la carpeta de destino.")
            return

        output_dir = self.file_selector.get_output_dir()
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

        params = self._get_operation_params(self._current_operation)

        self.process_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_text.append(f"Iniciando: {operation.name}...")

        self._last_output_dir = output_dir
        self._worker = Worker(operation, input_files, output_dir, params)
        self._worker.finished.connect(self._on_process_finished)
        self._worker.start()

    def _on_process_finished(self, success: bool, message: str):
        self.process_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            output_path = getattr(self, '_last_output_dir', None)
            path_info = f"\nGuardado en: {output_path}" if output_path else ""
            self.status_text.append(f"<span style='color: #689F38;'>✓ {message}{path_info}</span>")
            self.file_selector.clear_all()
            QMessageBox.information(self, "Éxito", f"{message}{path_info}")
        else:
            self.status_text.append(f"<span style='color: #D32F2F;'>✗ {message}</span>")
            QMessageBox.critical(self, "Error", message)
