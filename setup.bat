@echo off
REM SpotfyDown - Quick Start Setup Script for Windows

echo.
echo 🎵 SpotfyDown - Quick Start Setup
echo ==================================
echo.

REM Check Python version
echo ✓ Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ✗ Python not found. Please install Python 3.9+ from https://www.python.org/
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   Found Python: %PYTHON_VERSION%

REM Check FFmpeg
echo ✓ Checking FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo   ⚠️  FFmpeg not found. Please install it:
    echo      - Using Chocolatey: choco install ffmpeg
    echo      - Or download from: https://ffmpeg.org/download.html
    echo      - Then add to PATH environment variable
    exit /b 1
)
for /f "tokens=1,2,3" %%a in ('ffmpeg -version 2^>^&1 ^| findstr /R "ffmpeg version"') do (
    echo   Found: %%a %%b %%c
)

REM Create virtual environment
echo.
echo ✓ Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo   Virtual environment created in .\venv
) else (
    echo   Virtual environment already exists
)

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo ✓ Installing Python packages...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt

REM Summary
echo.
echo ==================================
echo ✅ Setup completed successfully!
echo.
echo 📝 Next steps:
echo    1. Activate: venv\Scripts\activate.bat
echo    2. Run: python app.py
echo    3. Open: http://localhost:5000
echo.
echo Happy downloading! 🎵
echo.
