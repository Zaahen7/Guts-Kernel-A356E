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
    "https://github.com/$OWNER/$REPO.git" \
    "$KERNEL_DIR"
