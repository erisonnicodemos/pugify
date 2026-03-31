#!/bin/bash
set -e

echo "🎵 Pugify Build Script - Render"
echo "==================================="
echo ""

# Step 1: Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Step 2: Download ffmpeg static binary
echo "⬇️  Downloading FFmpeg static binary..."

# Create ffmpeg directory
mkdir -p ffmpeg_bin
cd ffmpeg_bin

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    FFMPEG_URL="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
    echo "   Detected: x86_64 architecture"
elif [ "$ARCH" = "aarch64" ]; then
    FFMPEG_URL="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz"
    echo "   Detected: ARM64 architecture"
else
    echo "   ⚠️  Unsupported architecture: $ARCH"
    echo "   Falling back to apt-get install"
    apt-get update
    apt-get install -y ffmpeg
    exit 0
fi

# Download
wget -q $FFMPEG_URL -O ffmpeg.tar.xz 2>/dev/null || {
    echo "   ⚠️  Failed to download from johnvansickle.com"
    echo "   Attempting fallback download from GitHub..."
    apt-get update
    apt-get install -y ffmpeg
    cd ..
    exit 0
}

# Extract
echo "   Extracting FFmpeg..."
tar xf ffmpeg.tar.xz

# Find and set executable
if [ -f ffmpeg-*/ffmpeg ]; then
    cp ffmpeg-*/ffmpeg .
    chmod +x ffmpeg
    echo "   ✅ FFmpeg extracted and ready"
else
    echo "   ⚠️  FFmpeg binary not found in archive"
fi

cd ..

echo ""
echo "================================"
echo "✅ Build completed successfully!"
echo "================================"
