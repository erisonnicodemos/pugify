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

# Step 2: Install ffmpeg via apt-get (more reliable on Render)
echo "⬇️  Installing FFmpeg via apt-get..."
apt-get update -qq
apt-get install -y ffmpeg 2>&1 | grep -v "^Get:" | grep -v "^Hit:" || true

echo "✅ Build complete!"
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
