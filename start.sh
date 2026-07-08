#!/bin/bash
# start.sh - Railway startup script

echo "🚀 Starting WhatsApp Crash Empire Bot..."
echo "📂 Current directory: $(pwd)"
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🤖 Starting bot..."
python3 main.py