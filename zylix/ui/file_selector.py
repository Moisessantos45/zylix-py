import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(sys.executable).parent))

from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QFileDialog, QLineEdit, QApplication
)
from PySide6.QtCore import Signal, QTimer

from ..utils.file_manager import FileManager


class FileSelector(QWidget):

    files_changed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_files = []
        self._extensions = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Archivos seleccionados:"))
        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(120)
        layout.addWidget(self.file_list)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Agregar Archivos")
        self.add_btn.clicked.connect(self._select_files)
        btn_layout.addWidget(self.add_btn)

        self.remove_btn = QPushButton("Quitar")
        self.remove_btn.clicked.connect(self._remove_selected)
        btn_layout.addWidget(self.remove_btn)

        self.clear_btn = QPushButton("Limpiar Todo")
        self.clear_btn.clicked.connect(self._clear_all)
        btn_layout.addWidget(self.clear_btn)

        layout.addLayout(btn_layout)

        layout.addWidget(QLabel("Carpeta de salida:"))
        output_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        self.output_path.setPlaceholderText("Seleccionar carpeta de destino...")
        output_layout.addWidget(self.output_path)

        self.browse_output_btn = QPushButton("Examinar")
        self.browse_output_btn.clicked.connect(self._select_output_dir)
        output_layout.addWidget(self.browse_output_btn)

        layout.addLayout(output_layout)

    def set_extensions(self, extensions: list):
        self._extensions = extensions

    def _select_files(self):
        filters = "Archivos soportados ("
        if self._extensions:
            ext_filters = " ".join(f"*{e}" for e in self._extensions)
            filters += ext_filters + ")"
        else:
            filters += "*)"

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar archivos",
            "",
            filters
        )

        if files:
            for f in files:
                path = Path(f)
                if path not in self._selected_files:
                    self._selected_files.append(path)
                    self.file_list.addItem(str(path))
            self.files_changed.emit(list(self._selected_files))

    def _remove_selected(self):
        for item in self.file_list.selectedItems():
            path = Path(item.text())
            if path in self._selected_files:
                self._selected_files.remove(path)
            self.file_list.takeItem(self.file_list.row(item))
        self.files_changed.emit(self._selected_files)

    def _clear_all(self):
        self._selected_files.clear()
        self.file_list.clear()
        self.files_changed.emit(self._selected_files)

    def _select_output_dir(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta de salida",
            ""
        )
        if directory:
            self.output_path.setText(directory)

    def get_selected_files(self) -> list:
        return self._selected_files.copy()

    def get_output_dir(self) -> Path:
        path_text = self.output_path.text().strip()
        if path_text:
            return Path(path_text)
        return Path.cwd()

    def has_output_dir(self) -> bool:
        return bool(self.output_path.text().strip())

    def get_file_count(self) -> int:
        return self.file_list.count()

    def clear_all(self):
        self._selected_files.clear()
        self.file_list.clear()
        self.output_path.clear()
        self.files_changed.emit(self._selected_files)
