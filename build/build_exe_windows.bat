@echo off
chcp 65001 >nul
echo ====================================
echo   Zylix - Generador de EXE (Windows)
echo ====================================
echo.

REM Limpiar builds anteriores
echo [0/4] Limpiando builds anteriores...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "*.spec" del /q "*.spec"
for /d /r %%i in (__pycache__) do rmdir /s /q "%%i" 2>nul
echo.

REM Instalar dependencias
echo [1/4] Instalando dependencias...
pip install pyinstaller
pip install PySide6 pypdf pillow numpy pytesseract pdf2image scikit-image python-docx
echo.

REM Compilar con PyInstaller
echo [2/4] Compilando con PyInstaller...
pyinstaller --name "Zylix" ^
    --onefile ^
    --add-data "zylix;zylix" ^
    --icon="icon.ico" ^
    --noconfirm ^
    --clean ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=pypdf ^
    --hidden-import=numpy ^
    --hidden-import=pytesseract ^
    --hidden-import=skimage ^
    --hidden-import=skimage.io ^
    --hidden-import=skimage.color ^
    --hidden-import=skimage.morphology ^
    --hidden-import=pdf2image ^
    --hidden-import=docx ^
    zylix/__main__.py

if exist "dist\Zylix.exe" (
    echo.
    echo [3/4] EXE generado exitosamente!
    echo    Ubicacion: dist\Zylix.exe
    echo.
    echo [4/4] Copiando a carpeta build\windows...
    if not exist "build\windows" mkdir build\windows
    copy "dist\Zylix.exe" "build\windows\Zylix.exe" /Y
    if exist "icon.ico" copy "icon.ico" "build\windows\icon.ico" /Y
    echo.
    echo ====================================
    echo   EXE Listo para NSIS
    echo ====================================
    echo.
    echo El archivo Zylix.exe esta en: build\windows\
    echo Ahora puedes usar build_exe.sh en Linux para crear el instalador.
) else (
    echo.
    echo ERROR: No se pudo generar el EXE
    echo.
    pause
)
