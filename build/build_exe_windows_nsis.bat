@echo off
chcp 65001 >nul
echo ====================================
echo   Zylix - Generador de EXE (Windows)
echo ====================================
echo.

REM Verificar que existe el exe
if not exist "build\windows\Zylix.exe" (
    echo ERROR: No se encontro Zylix.exe
    echo Primero ejecuta: build_exe_windows.bat
    echo.
    pause
    exit /b 1
)

REM Limpiar builds anteriores
echo [1/3] Limpiando builds anteriores...
if exist "build\windows\zylix-setup.exe" del /q "build\windows\zylix-setup.exe"
echo.

REM Verificar NSIS
where makensis >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: NSIS no esta instalado.
    echo Instala NSIS desde: https://nsis.sourceforge.io/Download
    echo.
    pause
    exit /b 1
)

REM Copiar archivos necesarios
echo [2/3] Preparando archivos...
if exist "icon.ico" copy /Y "icon.ico" "build\windows\icon.ico" >nul
if exist "LICENSE" copy /Y "LICENSE" "build\windows\LICENSE" >nul

REM Crear script NSIS
echo [3/3] Generando instalador con NSIS...

cd build\windows

(
echo !include "MUI2.nsh"
echo.
echo !define MUI_ICON "icon.ico"
echo !define MUI_UNICON "icon.ico"
echo.
echo !define APPNAME "Zylix"
echo !define APPVERSION "2.0.0"
echo !define COMPANYNAME "Zylix Team"
echo !define EXENAME "Zylix.exe"
echo.
echo Name "${APPNAME}"
echo OutFile "zylix-setup.exe"
echo InstallDir "$PROGRAMFILES64\${APPNAME}"
echo RequestExecutionLevel admin
echo.
echo BrandingText "${COMPANYNAME}"
echo.
echo !define MUI_ABORTWARNING
echo !define MUI_FINISHPAGE_RUN "$INSTDIR\${EXENAME}"
echo !define MUI_FINISHPAGE_RUN_TEXT "Ejecutar ${APPNAME}"
echo !define MUI_FINISHPAGE_RUN_NOTCHECKED
echo.
echo !insertmacro MUI_PAGE_WELCOME
echo !insertmacro MUI_PAGE_DIRECTORY
echo !insertmacro MUI_PAGE_INSTFILES
echo !insertmacro MUI_PAGE_FINISH
echo.
echo !insertmacro MUI_UNPAGE_CONFIRM
echo !insertmacro MUI_UNPAGE_INSTFILES
echo.
echo !insertmacro MUI_LANGUAGE "Spanish"
echo.
echo Section "Main"
echo   SetShellVarContext all
echo   SetOutPath "$INSTDIR"
echo.
echo   File "Zylix.exe"
echo   WriteUninstaller "$INSTDIR\Uninstall.exe"
echo.
echo   CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${EXENAME}"
echo   CreateDirectory "$SMPROGRAMS\${APPNAME}"
echo   CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${EXENAME}"
echo   CreateShortcut "$SMPROGRAMS\${APPNAME}\Desinstalar ${APPNAME}.lnk" "$INSTDIR\Uninstall.exe"
echo.
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\Uninstall.exe$\" /S"
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$INSTDIR"
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$INSTDIR\${EXENAME}"
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${APPVERSION}"
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
echo   WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
echo   WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
echo SectionEnd
echo.
echo Section "Uninstall"
echo   SetShellVarContext all
echo   Delete "$DESKTOP\${APPNAME}.lnk"
echo   Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
echo   Delete "$SMPROGRAMS\${APPNAME}\Desinstalar ${APPNAME}.lnk"
echo   RMDir "$SMPROGRAMS\${APPNAME}"
echo.
echo   DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
echo.
echo   RMDir /r "$INSTDIR"
echo SectionEnd
) > installer.nsi

REM Compilar con NSIS
makensis installer.nsi

if exist "zylix-setup.exe" (
    echo.
    echo ====================================
    echo   Instalador generado exitosamente!
    echo ====================================
    echo.
    echo Ubicacion: build\windows\zylix-setup.exe
) else (
    echo.
    echo ERROR: No se pudo generar el instalador
)

cd ..\..
echo.
pause
