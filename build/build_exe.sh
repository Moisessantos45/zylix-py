#!/bin/bash

set -e

VERSION="2.0.0"
BUILD_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$BUILD_DIR")"

echo "=== Building Zylix EXE Installer (Windows) ==="

# Check for Windows executable
EXE_PATH="$PROJECT_DIR/dist/Zylix.exe"
if [ ! -f "$EXE_PATH" ]; then
    EXE_PATH="$PROJECT_DIR/dist/Zylix"
fi

if [ ! -f "$EXE_PATH" ]; then
    echo "[!] Windows executable not found at dist/Zylix.exe"
    echo "[!] PyInstaller on Linux cannot cross-compile to Windows."
    echo "[!] You need to build the Windows .exe on a Windows machine first."
    echo ""
    echo "Options:"
    echo "  1. Build on Windows with: pyinstaller --onefile --icon=icon.ico zylix/__main__.py"
    echo "  2. Copy the resulting Zylix.exe to: $PROJECT_DIR/dist/"
    echo "  3. Run this script again."
    exit 1
fi

echo "[1/3] Found executable: $EXE_PATH"

# Clean old build
echo "[0/3] Cleaning old builds..."
rm -rf "$BUILD_DIR/windows"
rm -f "$BUILD_DIR/zylix-${VERSION}-setup.exe"

# Create Windows distribution folder
mkdir -p "$BUILD_DIR/windows"

# Copy executable
cp "$EXE_PATH" "$BUILD_DIR/windows/Zylix.exe"

# Copy icon if exists
if [ -f "$PROJECT_DIR/icon.ico" ]; then
    cp "$PROJECT_DIR/icon.ico" "$BUILD_DIR/windows/"
fi

# Create NSIS script
cat > "$BUILD_DIR/windows/installer.nsi" << 'EOF'
!include "MUI2.nsh"

!define MUI_ICON "build\windows\icon.ico"
!define MUI_UNICON "build\windows\icon.ico"

!define APPNAME "Zylix"
!define APPVERSION "0.1.0"
!define COMPANYNAME "Zylix Team"
!define EXENAME "Zylix.exe"

Name "${APPNAME}"
OutFile "zylix-setup.exe"
InstallDir "$PROGRAMFILES64\${APPNAME}"
RequestExecutionLevel admin

BrandingText "${COMPANYNAME}"

!define MUI_ABORTWARNING
!define MUI_FINISHPAGE_RUN "$INSTDIR\${EXENAME}"
!define MUI_FINISHPAGE_RUN_TEXT "Ejecutar ${APPNAME}"
!define MUI_FINISHPAGE_RUN_NOTCHECKED

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Spanish"

Section "Main"
  SetShellVarContext all
  SetOutPath "$INSTDIR"

  File "build\windows\Zylix.exe"
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${EXENAME}"
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${EXENAME}"
  CreateShortcut "$SMPROGRAMS\${APPNAME}\Desinstalar ${APPNAME}.lnk" "$INSTDIR\Uninstall.exe"

  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\Uninstall.exe$\" /S"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$INSTDIR\${EXENAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${APPVERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
SectionEnd

Section "Uninstall"
  SetShellVarContext all
  Delete "$DESKTOP\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\${APPNAME}\Desinstalar ${APPNAME}.lnk"
  RMDir "$SMPROGRAMS\${APPNAME}"

  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

  RMDir /r "$INSTDIR"
SectionEnd
EOF

echo "[2/3] NSIS script created"

# Build installer
echo "[3/3] Building installer with NSIS..."
cd "$PROJECT_DIR"
makensis "$BUILD_DIR/windows/installer.nsi"

echo ""
echo "=== EXE Installer Created ==="
echo "File: $BUILD_DIR/windows/zylix-setup.exe"
