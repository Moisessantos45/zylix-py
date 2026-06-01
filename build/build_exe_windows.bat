@echo off
chcp 65001 >nul
echo ====================================
echo   Zylix - Generador de EXE (Windows)
echo ====================================
echo.

REM Verificar poppler
echo [0/5] Verificando poppler...
where pdftoppm >nul 2>&1
if %errorlevel% neq 0 (
    echo AVISO: Poppler no encontrado. Es necesario para PDF a Imagen.
    echo.
    echo Instalando poppler via chocolatey...
    choco install poppler -y
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo instalar poppler automaticamente.
        echo Instala poppler manualmente desde:
        echo   https://github.com/oschwartz10612/poppler-windows/releases
        echo.
        echo O usa chocolatey: winget install AlexandruPopescu.poppler
        pause
    )
)
echo.

REM Limpiar builds anteriores
echo [1/5] Limpiando builds anteriores...
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "build\Zylix" rmdir /s /q "build\Zylix" 2>nul
if exist "build\linux" rmdir /s /q "build\linux" 2>nul
if exist "build\windows\zylix-setup.exe" del /q "build\windows\zylix-setup.exe" 2>nul
if exist "*.spec" del /q "*.spec" 2>nul
for /d /r %%i in (__pycache__) do rmdir /s /q "%%i" 2>nul
echo.

REM Instalar dependencias
echo [2/5] Instalando dependencias...
pip install pyinstaller
pip install PySide6 pypdf pillow numpy pytesseract pdf2image scikit-image python-docx
echo.

REM Compilar con PyInstaller
echo [3/5] Compilando con PyInstaller...
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
    echo [4/5] EXE generado exitosamente!
    echo    Ubicacion: dist\Zylix.exe
    echo.
    echo [5/5] Copiando a carpeta build\windows...
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
