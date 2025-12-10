#!/bin/bash
# Quick Start Script for Gitinsky Support Bot (Linux/Mac)

echo ""
echo "================================================"
echo "  Gitinsky Support Bot - Quick Start"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo "[1/5] Checking Python version..."
python3 --version

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "[2/5] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
else
    echo ""
    echo "[2/5] Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "[3/5] Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "[4/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "Please edit .env file with your configuration before running the bot"
    exit 0
fi

# Populate knowledge base if database doesn't exist
if [ ! -f "gitinsky_bot.db" ]; then
    echo ""
    echo "[5/5] Initializing knowledge base..."
    python populate_knowledge.py
    if [ $? -ne 0 ]; then
        echo "WARNING: Failed to populate knowledge base"
        echo "You can run 'python populate_knowledge.py' manually later"
    fi
else
    echo ""
    echo "[5/5] Database already exists, skipping initialization"
fi

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "To start the bot, run: python main.py"
echo ""
echo "Make sure you have configured .env with:"
echo "  - TELEGRAM_BOT_TOKEN"
echo "  - DEEPSEEK_API_KEY"
echo "  - SMTP settings"
echo "  - COMPANY_EMAIL_DOMAIN"
echo ""
