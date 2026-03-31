#!/bin/bash
set -e

echo "🎵 Pugify Build Script - Render"
echo "==================================="
echo ""

# Step 0: Ensure pip and setuptools are up to date
echo "📦 Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Step 1: Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Step 2: Try to install ffmpeg (skip if fails, may already exist)
echo "⬇️  Checking for FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg already available"
else
    echo "Attempting to install FFmpeg..."
    apt-get install -y ffmpeg 2>/dev/null || {
        echo "⚠️  apt-get install failed, attempting apt-get with cache..."
        apt-get install -y --no-install-recommends ffmpeg 2>/dev/null || {
            echo "⚠️  FFmpeg installation skipped - will try fallback"
        }
    }
fi

# Verify FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg available: $(ffmpeg -version | head -n1)"
else
    echo "⚠️  FFmpeg not found - spotdl might fail"
fi

echo "✅ Build complete!"
