VERDE_MANZANA = "#8BC34A"
VERDE_OSCURO = "#689F38"
VERDE_CLARO = "#C5E1A5"
VERDE_MUY_CLARO = "#F1F8E9"
BLANCO = "#FFFFFF"
GRIS_SUAVE = "#E8F5E9"
TEXTO_PRINCIPAL = "#33691E"
TEXTO_SECUNDARIO = "#558B2F"
BORDE = "#AED581"

SIDEBAR_STYLE = f"""
QWidget {{
    background-color: {VERDE_MANZANA};
    color: {BLANCO};
}}
QPushButton {{
    background-color: transparent;
    color: {BLANCO};
    border: none;
    padding: 10px 15px;
    text-align: left;
    font-size: 14px;
    border-radius: 5px;
}}
QPushButton:hover {{
    background-color: {VERDE_OSCURO};
}}
QPushButton:selected {{
    background-color: {VERDE_OSCURO};
    font-weight: bold;
}}
QLabel {{
    color: {TEXTO_PRINCIPAL};
}}
"""

MAIN_STYLE = f"""
QMainWindow {{
    background-color: {BLANCO};
}}
QWidget#central_widget {{
    background-color: {BLANCO};
}}
QPushButton#process_btn {{
    background-color: {VERDE_MANZANA};
    color: {BLANCO};
    border: none;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: bold;
    border-radius: 8px;
}}
QPushButton#process_btn:hover {{
    background-color: {VERDE_OSCURO};
}}
QPushButton#process_btn:disabled {{
    background-color: {BORDE};
}}
QPushButton#select_btn {{
    background-color: {VERDE_CLARO};
    color: {TEXTO_PRINCIPAL};
    border: 1px solid {BORDE};
    padding: 10px 20px;
    font-size: 13px;
    border-radius: 6px;
}}
QPushButton#select_btn:hover {{
    background-color: {VERDE_MANZANA};
    color: {BLANCO};
}}
QLineEdit {{
    border: 2px solid {VERDE_CLARO};
    border-radius: 6px;
    padding: 8px 12px;
    background-color: {BLANCO};
    color: {TEXTO_PRINCIPAL};
}}
QLineEdit:focus {{
    border-color: {VERDE_MANZANA};
}}
QComboBox {{
    border: 2px solid {VERDE_CLARO};
    border-radius: 6px;
    padding: 8px 12px;
    background-color: {BLANCO};
    color: {TEXTO_PRINCIPAL};
}}
QComboBox:focus {{
    border-color: {VERDE_MANZANA};
}}
QSlider::groove:horizontal {{
    border: 1px solid {VERDE_CLARO};
    height: 8px;
    background: {VERDE_CLARO};
    border-radius: 4px;
}}
QSlider::handle:horizontal {{
    background: {VERDE_MANZANA};
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}}
QListWidget {{
    border: 2px solid {VERDE_CLARO};
    border-radius: 6px;
    background-color: {BLANCO};
    color: {TEXTO_PRINCIPAL};
    padding: 5px;
}}
QListWidget::item {{
    padding: 5px;
    border-radius: 3px;
}}
QListWidget::item:selected {{
    background-color: {VERDE_CLARO};
    color: {TEXTO_PRINCIPAL};
}}
QScrollArea {{
    border: none;
    background-color: {BLANCO};
}}
QGroupBox {{
    border: 2px solid {VERDE_CLARO};
    border-radius: 8px;
    margin-top: 15px;
    padding: 15px;
    background-color: {BLANCO};
    color: {TEXTO_PRINCIPAL};
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    color: {TEXTO_PRINCIPAL};
}}
"""

CATEGORIA_HEADER_STYLE = f"""
QLabel {{
    color: {BLANCO};
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    padding: 5px 15px;
    background-color: {VERDE_OSCURO};
}}
"""
