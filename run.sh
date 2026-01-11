#!/bin/bash

# 🚀 Quick Start Script for Streamlit Soccer Platform

echo "⚽ Starting Streamlit Soccer Platform..."
echo ""

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "✅ Activating virtual environment..."
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "💡 Please run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "💡 Please create .env with your API keys:"
    echo "   FOOTBALL_DATA_API_KEY=your_key"
    echo "   SCOREBAT_API_KEY=your_key"
    echo ""
fi

# Run Streamlit
echo "🚀 Launching application..."
echo ""
streamlit run app.py
