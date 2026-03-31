#!/bin/bash
# SpotfyDown - Quick Start Setup Script

set -e

echo "🎵 SpotfyDown - Quick Start Setup"
echo "=================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "  Found Python: $python_version"

# Check FFmpeg
echo "✓ Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version | head -n1)
    echo "  Found: $ffmpeg_version"
else
    echo "  ⚠️  FFmpeg not found. Please install it:"
    echo "     - Windows: choco install ffmpeg"
    echo "     - macOS: brew install ffmpeg"
    echo "     - Linux: sudo apt-get install ffmpeg"
    exit 1
fi

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "  Virtual environment created in ./venv"
else
    echo "  Virtual environment already exists"
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "✓ Installing Python packages..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt

# Summary
echo ""
echo "=================================="
echo "✅ Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate: source venv/bin/activate"
echo "   2. Run: python app.py"
echo "   3. Open: http://localhost:5000"
echo ""
echo "Happy downloading! 🎵"
