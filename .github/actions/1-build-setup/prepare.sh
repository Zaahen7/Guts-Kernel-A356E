#!/bin/bash
set -euo pipefail

# Install dependencies
echo "Installing dependencies..."
sudo apt update
sudo apt-get install -y libyaml-dev
echo "Done :v"

# Prepare directories
echo "Preparing directories..."
rm -rf "$KERNEL_DIR" "$TOOLCHAIN_DIR" "$ANYKERNEL3_DIR"
mkdir "$KERNEL_DIR" "$TOOLCHAIN_DIR" "$ANYKERNEL3_DIR"
echo "Done :v"

# Clone Kernel Source
echo "Cloning Kernel Source..."
git clone \
    --depth 1 \
    --single-branch \
    --branch "$KERNEL_BRANCH" \
    "$KERNEL_SOURCE" \
    "$KERNEL_DIR"
echo "Done :v"

# Clone Toolchain
echo "Cloning Toolchain..."
git clone \
    --depth 1 \
    --single-branch \
    --branch "$TOOLCHAIN_BRANCH" \
    "$TOOLCHAIN_SOURCE" \
    "$TOOLCHAIN_DIR"
echo "Done :v"

# Setup Toolchain
echo "Toolchain Setup..."
for archive in "$TOOLCHAIN_DIR"/*.tar.xz; do
  echo "Extracting: $(basename "$archive")"
  tar -xJf "$archive" -C "$TOOLCHAIN_DIR"
  rm -f "$archive"
done
mv "$TOOLCHAIN_DIR/toolchain" "$KERNEL_DIR"
echo "Done :v"

# Clone Anykernel3
echo "Cloning Anykernel3..."
git clone \
    --depth 1 \
    --single-branch \
    --branch "$ANYKERNEL3_BRANCH" \
    "$ANYKERNEL3_SOURCE" \
    "$ANYKERNEL3_DIR"
echo "Done :v"

# Extract Kernel Version from MAKEFILE
KERNEL_VERSION=$(make -s -C "$KERNEL_DIR" kernelversion)
echo "Kernel version: $KERNEL_VERSION"
echo "KERNEL_VERSION=$KERNEL_VERSION" >> "$GITHUB_ENV"

# Edit update-binary from Anykernel3
echo "Editing update-binary..."
sed -i "s/Zaahen7/$ONEUI_VERSION/g" "$ANYKERNEL3_DIR/META-INF/com/google/android/update-binary"
sed -i "s/7nehaaZ/$KERNEL_VERSION/g" "$ANYKERNEL3_DIR/META-INF/com/google/android/update-binary"
echo "update-binary modified succesfully"
