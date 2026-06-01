import sys
import os
from pathlib import Path

# Add parent directory to path for PyInstaller
if getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(sys.executable).parent))

from PySide6.QtWidgets import QApplication

try:
    from .ui.main_window import MainWindow
except ImportError:
    from zylix.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Zylix")
    app.setApplicationVersion("0.1.0")

    # Forzar estilo Fusion para consistencia entre plataformas
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
