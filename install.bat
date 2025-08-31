@echo off
chcp 65001 > nul
title RFID-emulator Installer
color 0A

:: 1. Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ from python.org
    start "" "https://www.python.org/downloads/"
    pause
    exit /b 1
)

:: 2. Create virtual environment
echo [2/4] Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create .venv
    pause
    exit /b 1
)

:: 3. Install dependencies
echo [3/4] Installing dependencies...
call .venv\Scripts\activate
python -m pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo [WARNING] requirements.txt not found, installing default packages
    pip install fastapi uvicorn requests pytest
)

:: 4. Initialize DB
echo [4/4] Initializing database...
python init_db.py

echo Installation completed successfully!
echo To start the system:
echo   .venv\Scripts\activate
echo   python server.py
pause