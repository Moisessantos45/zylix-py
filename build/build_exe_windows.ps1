# Zylix - Generador de EXE (Windows)
# Ejecutar desde PowerShell: .\build_exe_windows.ps1

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  Zylix - Generador de EXE (Windows)" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Limpiar builds anteriores
Write-Host "[0/4] Limpiando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build\Zylix") { Remove-Item -Recurse -Force "build\Zylix" }
if (Test-Path "build\linux") { Remove-Item -Recurse -Force "build\linux" }
if (Test-Path "*.spec") { Remove-Item "*.spec" }
Get-ChildItem -Path "." -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force 2>$null
Write-Host ""

# Instalar dependencias
Write-Host "[1/4] Instalando dependencias..." -ForegroundColor Yellow
uv pip install pyinstaller PySide6 pypdf pillow numpy pytesseract pdf2image scikit-image python-docx
Write-Host ""

# Compilar con PyInstaller
Write-Host "[2/4] Compilando con PyInstaller..." -ForegroundColor Yellow
uv run pyinstaller --name "Zylix" `
    --onefile `
    --add-data "zylix;zylix" `
    --icon="icon.ico" `
    --noconfirm `
    --clean `
    --hidden-import=PIL `
    --hidden-import=PIL.Image `
    --hidden-import=pypdf `
    --hidden-import=numpy `
    --hidden-import=pytesseract `
    --hidden-import=skimage `
    --hidden-import=skimage.io `
    --hidden-import=skimage.color `
    --hidden-import=skimage.morphology `
    --hidden-import=pdf2image `
    --hidden-import=docx `
    zylix/__main__.py

if (Test-Path "dist\Zylix.exe") {
    Write-Host ""
    Write-Host "[3/4] EXE generado exitosamente!" -ForegroundColor Green
    Write-Host "    Ubicacion: dist\Zylix.exe" -ForegroundColor Green
    Write-Host ""

    Write-Host "[4/4] Copiando a carpeta build\windows..." -ForegroundColor Yellow
    if (-not (Test-Path "build\windows")) { New-Item -ItemType Directory -Path "build\windows" | Out-Null }
    Copy-Item "dist\Zylix.exe" "build\windows\Zylix.exe" -Force
    if (Test-Path "icon.ico") { Copy-Item "icon.ico" "build\windows\icon.ico" -Force }

    Write-Host ""
    Write-Host "====================================" -ForegroundColor Cyan
    Write-Host "  EXE Listo para NSIS" -ForegroundColor Green
    Write-Host "====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "El archivo Zylix.exe esta en: build\windows\" -ForegroundColor Green
    Write-Host "Ahora puedes usar build_exe.sh en Linux para crear el instalador." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "ERROR: No se pudo generar el EXE" -ForegroundColor Red
    Write-Host ""
    Read-Host "Presiona Enter para salir"
}
