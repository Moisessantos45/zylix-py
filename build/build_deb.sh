#!/bin/bash

set -e

VERSION="2.0.0"
BUILD_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$BUILD_DIR")"

echo "=== Building Zylix DEB Package ==="

# Save script path before cleaning
SCRIPT_PATH="$BUILD_DIR/build_deb.sh"

# Clean build directories (except this script)
echo "[0/4] Cleaning build directories..."
rm -rf "$PROJECT_DIR/build/Zylix" "$PROJECT_DIR/build/linux"
rm -rf "$PROJECT_DIR/dist" "$PROJECT_DIR/__pycache__"
rm -rf "$PROJECT_DIR/zylix/__pycache__" "$PROJECT_DIR/zylix"/*/__pycache__
rm -f "$PROJECT_DIR"/*.spec

# Recreate build directory structure
mkdir -p "$BUILD_DIR/linux/DEBIAN"
mkdir -p "$BUILD_DIR/linux/usr/local/bin"
mkdir -p "$BUILD_DIR/linux/usr/local/share/zylix"
mkdir -p "$BUILD_DIR/linux/usr/share/applications"

# Create DEBIAN control file
cat > "$BUILD_DIR/linux/DEBIAN/control" << EOF
Package: zylix
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Zylix Team
Description: Zylix - File Manipulation Tool
 A tool for PDF and image manipulation.
EOF

# Install pyinstaller and build
echo "[1/4] Building executable..."
cd "$PROJECT_DIR"
uv pip install pyinstaller
uv run pyinstaller --name "Zylix" \
    --onefile \
    --add-data "zylix:zylix" \
    --icon="icon.png" \
    --noconfirm \
    --clean \
    --hidden-import=PIL \
    --hidden-import=PIL.Image \
    --hidden-import=pypdf \
    --hidden-import=numpy \
    --hidden-import=pytesseract \
    --hidden-import=skimage \
    --hidden-import=skimage.io \
    --hidden-import=skimage.color \
    --hidden-import=skimage.morphology \
    --hidden-import=pdf2image \
    --hidden-import=docx \
    zylix/__main__.py
echo "[2/4] Executable built."

# Copy files
echo "[3/4] Copying files..."

# Copy executable
cp "$PROJECT_DIR/dist/Zylix" "$BUILD_DIR/linux/usr/local/bin/"
chmod +x "$BUILD_DIR/linux/usr/local/bin/Zylix"

# Copy icon
cp "$PROJECT_DIR/icon.png" "$BUILD_DIR/linux/usr/local/share/zylix/"

# Copy desktop file
cp "$PROJECT_DIR/zylix.desktop" "$BUILD_DIR/linux/usr/share/applications/"

echo "[4/4] Building DEB package..."
cd "$BUILD_DIR/linux"
dpkg-deb --build . "$BUILD_DIR/zylix_${VERSION}_amd64.deb"

echo ""
echo "=== DEB Package Created ==="
echo "File: $BUILD_DIR/zylix_${VERSION}_amd64.deb"
echo ""
echo "To install: sudo dpkg -i $BUILD_DIR/zylix_${VERSION}_amd64.deb"
echo "To uninstall: sudo dpkg -r zylix"
