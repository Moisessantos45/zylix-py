# Zylix

Aplicación de escritorio para manipulación de PDFs e imágenes.

## Características

- **100% offline** - Sin conexión a internet requerida
- **Multiplataforma** - Funciona en Windows y Linux
- **Sin librerías de pago** - Totalmente gratuito

## Funcionalidades

### PDF
- PDF a Imagen
- Imagen a PDF
- Unir PDFs
- Dividir PDF
- Comprimir PDF
- Extraer Texto
- Agregar Marca de Agua
- Rotar PDF

### Imagen
- Cambiar Formato (PNG, JPG, WEBP, BMP)
- Optimizar con calidad seleccionable
- Rotar
- Remover Fondo
- OCR (extracción de texto)
- Imagen a Word

## Instalación

### Linux (.deb)

- **Descarga:** [zylix_2.0.0_amd64.deb](https://drive.google.com/file/d/1g_O9x8-QcMa0AkOm5liClDbscucFvrsV/view?usp=sharing)

```bash
sudo dpkg -i zylix_2.0.0_amd64.deb
```

Para desinstalar:
```bash
sudo dpkg -r zylix
```

### Windows

- **Descarga:** [zylix-setup-2.0.0.exe](https://drive.google.com/file/d/1urMFNchNGvD-3dL1ZdrCQoV865OeXWVk/view?usp=sharing)

Ejecuta el instalador `zylix-setup.exe`

## Desarrollo

### Requisitos

- Python >= 3.10
- uv (gestor de paquetes)
- Tesseract (para OCR)
- Poppler (para PDF a Imagen)

### Instalar dependencias del sistema

**Ubuntu/Debian:**
```bash
sudo apt install tesseract-ocr poppler-utils
```

**macOS:**
```bash
brew install tesseract poppler
```

**Windows:**

1. **Tesseract OCR** - Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
   ```powershell
   # Verificar instalación
   tesseract -v
   ```

2. **Poppler (para PDF a imagen)** - Descargar desde: https://github.com/oschwartz10612/poppler-windows/releases
   - Descargar el ZIP que diga "Release"
   - Descomprimir y colocar en `C:\poppler\Library\bin`
   - Agregar al PATH de usuario:

   ```powershell
   $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
   $newPath = "C:\poppler\Library\bin"

   if (-not ($currentPath -split ';' -contains $newPath)) {
       $newEnvPath = ($currentPath -split ';' | Where-Object { $_ -ne "" }) -join ';'
       $newEnvPath += ";" + $newPath
       [Environment]::SetEnvironmentVariable("Path", $newEnvPath, "User")
   }
   ```

   - Verificar instalación:
   ```powershell
   pdfinfo -v
   pdftotext -v
   ```

### Instalar dependencias Python y ejecutar

**Linux/macOS:**
```bash
# Crear entorno virtual
uv venv .venv
source .venv/bin/activate

# Instalar dependencias
uv sync

# Ejecutar
python -m zylix
```

**Windows (PowerShell):**
```powershell
# Crear entorno virtual
uv venv .venv

# Activar entorno
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
uv sync

# Ejecutar
python -m zylix
```

## Compilación

### Linux - Generar .deb

```bash
./build/build_deb.sh
```

El instalador se genera en: `build/zylix_0.1.0_amd64.deb`

### Windows - Generar .exe

**Opción 1: Todo en Windows (requiere NSIS instalado)**

1. Instalar NSIS desde: https://nsis.sourceforge.io/Download

2. Ejecutar desde CMD o PowerShell:
```bash
.\build\build_exe_windows.bat
```
   - Genera `build\windows\Zylix.exe`

3. Luego ejecutar:
```bash
.\build\build_exe_windows_nsis.bat
```
   - Genera `build\windows\zylix-setup.exe`

**Opción 2: Compilar en Windows, crear installer en Linux**

1. En Windows:
```bash
.\build\build_exe_windows.bat
```

2. Copiar `build\windows\Zylix.exe` a tu Linux en `dist/`

3. En Linux:
```bash
./build/build_exe.sh
```

El instalador se genera en: `build/windows/zylix-setup.exe`

### Estructura de scripts de build

```
build/
├── build_deb.sh                  # Genera .deb para Linux
├── build_exe.sh                 # Genera instalador .exe en Linux (requiere Zylix.exe en dist/)
├── build_exe_windows.bat        # Compila Zylix.exe en Windows (CMD)
├── build_exe_windows.ps1        # Compila Zylix.exe en Windows (PowerShell)
├── build_exe_windows_nsis.bat   # Genera instalador .exe en Windows (requiere NSIS)
└── windows/
    ├── Zylix.exe                 # (generado por build_exe_windows.bat)
    ├── icon.ico                  # Icono para el instalador
    └── zylix-setup.exe           # Instalador NSIS generado
```

## Tecnologías

- **UI:** PySide6
- **Imágenes:** Pillow
- **PDFs:** pypdf
- **OCR:** pytesseract
- **Procesamiento de imagen:** scikit-image
- **Conversión PDF a imagen:** pdf2image + poppler
- **Documentos Word:** python-docx
- **Build:** PyInstaller, NSIS

## Autor

**Moises Santos Hernandez**

- GitHub: https://github.com/Moisessantos45
- Repositorio: https://github.com/Moisessantos45/zylix-py
- Web: https://portafolio.mmabitec.me/

## Licencia

Este proyecto está bajo la licencia **Non-Commercial License**. Consulta el archivo `LICENSE` para más detalles.

Se permite:
- Uso educativo
- Uso personal
- Investigación y desarrollo
- Crear obras derivadas basadas en este software

No se permite uso comercial. Ver `LICENSE` para términos completos.
