@echo off
echo Installing Python dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install some packages
    echo Trying alternative installation method...
    pip install --user -r requirements.txt
)

echo.
echo Installation completed!
echo.
echo To run the app, use: python app.py
echo.
pause
