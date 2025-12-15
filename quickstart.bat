@echo off
REM Quick Start Script for Gitinsky Support Bot (Windows)

echo.
echo ================================================
echo   Gitinsky Support Bot - Quick Start
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo.
    echo [2/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
) else (
    echo.
    echo [2/5] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found
    echo Please copy .env.example to .env and configure it with your credentials
    echo.
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env file with your configuration before running the bot
    pause
    exit /b 0
)

REM Populate knowledge base if database doesn't exist
if not exist "gitinsky_bot.db" (
    echo.
    echo [5/5] Initializing knowledge base...
    python populate_knowledge.py
    if errorlevel 1 (
        echo WARNING: Failed to populate knowledge base
        echo You can run 'python populate_knowledge.py' manually later
    )
) else (
    echo.
    echo [5/5] Database already exists, skipping initialization
)

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To start the bot, run: python main.py
echo.
echo Make sure you have configured .env with:
echo   - TELEGRAM_BOT_TOKEN
echo   - OPENROUTER_API_KEY
echo   - SMTP settings
echo   - COMPANY_EMAIL_DOMAIN
echo.
pause
