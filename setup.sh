#!/bin/bash

# Setup script for the matchmaking server

echo "🎮 Setting up Matchmaking Server..."
echo "=================================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the server:"
echo "     python server.py"
echo ""
echo "To deactivate the virtual environment later:"
echo "     deactivate"
