#!/bin/bash

# HDR Photo Maker Environment Setup & Launch Script
# Compatible with Linux and macOS

set -e  # Exit on error

echo "📸 Setting up HDR Photo Maker environment..."

# Create virtual environment
echo "📦 Creating Python virtual environment (hdr_env)..."
python3 -m venv hdr_env
source hdr_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies (Pillow, OpenCV, NumPy)..."
pip install pillow opencv-python numpy

# Check tkinter availability
echo "🔍 Checking tkinter..."
python3 -c "import tkinter" 2>/dev/null && echo "✅ Tkinter OK" || echo "⚠️  Tkinter missing! Install with: brew install python-tk OR sudo apt install python3-tk"

# Tip for OpenCV contrib modules
echo "ℹ️ If tone mapping features are missing, consider: pip install opencv-contrib-python"

# Find and run the main Python file
APP_FILE="hdr_photo_maker.py"
if [[ -f "$APP_FILE" ]]; then
  echo "🚀 Launching HDR Photo Maker..."
  python "$APP_FILE"
else
  echo "❌ ERROR: Cannot find $APP_FILE in this directory."
  echo "Please run this script from the folder where your Python file is located."
  exit 1
fi
