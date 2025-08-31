@echo off
echo Starting YouTube Info App...
echo.

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing requirements first...
    call install.bat
)

echo Starting the application...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
