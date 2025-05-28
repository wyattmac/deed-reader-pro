@echo off
title Deed Reader Pro - Smart Launcher
color 0A

echo ============================================
echo     DEED READER PRO - SMART LAUNCHER
echo ============================================
echo.
echo [INFO] Running from scripts directory - adjusting paths...
echo.

:: Check for Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.9 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
echo [OK] Python found!

:: Check for Node.js
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH!
    echo.
    echo Please install Node.js 18 or higher from:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
)
echo [OK] Node.js found!

:: Check/Create backend virtual environment
echo [3/6] Checking backend environment...
if not exist "deed-reader-web\backend\venv" (
    echo Creating Python virtual environment...
    cd deed-reader-web\backend
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        echo Try running as Administrator.
        pause
        exit /b 1
    )
    cd ..\..
)
echo [OK] Backend environment ready!

:: Install/Update backend dependencies
echo [4/6] Checking backend dependencies...
cd deed-reader-web\backend
call venv\Scripts\activate.bat >nul 2>&1

:: Check if all required packages are installed
python -c "import flask, anthropic, PyPDF2" >nul 2>&1
if errorlevel 1 (
    echo Installing/updating backend dependencies...
    python -m pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install backend dependencies!
        echo Check your internet connection and try again.
        pause
        exit /b 1
    )
)
cd ..\..
echo [OK] Backend dependencies installed!

:: Check/Install frontend dependencies
echo [5/6] Checking frontend dependencies...
if not exist "deed-reader-web\frontend\node_modules" (
    echo Installing frontend dependencies...
    cd deed-reader-web\frontend
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies!
        echo Check your internet connection and try again.
        pause
        exit /b 1
    )
    cd ..\..
)
echo [OK] Frontend dependencies installed!

:: Check if ports are already in use
echo [6/6] Checking port availability...
netstat -an | findstr :5000 | findstr LISTENING >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 5000 is already in use!
    echo.
    echo Do you want to kill the existing process? (Y/N)
    choice /C YN /M "Your choice"
    if errorlevel 2 goto skip_backend_kill
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)
:skip_backend_kill

netstat -an | findstr :3000 | findstr LISTENING >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 3000 is already in use!
    echo.
    echo Do you want to kill the existing process? (Y/N)
    choice /C YN /M "Your choice"
    if errorlevel 2 goto skip_frontend_kill
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)
:skip_frontend_kill

:: Start the servers
cls
echo ============================================
echo     STARTING DEED READER PRO
echo ============================================
echo.

:: Start backend with error handling
echo Starting backend server...
start "Deed Reader Backend" cmd /c "cd deed-reader-web\backend && venv\Scripts\activate && python app.py || (echo. && echo [ERROR] Backend crashed! Check the error above. && pause)"

:: Wait for backend to initialize
echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

:: Check if backend started successfully
curl -s http://localhost:5000/api/health >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Backend may not have started properly.
    echo Continuing anyway...
) else (
    echo [OK] Backend is running!
)

:: Start frontend with error handling
echo Starting frontend server...
start "Deed Reader Frontend" cmd /c "cd deed-reader-web\frontend && npm start || (echo. && echo [ERROR] Frontend crashed! Check the error above. && pause)"

:: Final message
echo.
echo ============================================
echo     DEED READER PRO IS STARTING
echo ============================================
echo.
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:3000
echo.
echo The browser should open automatically in a few seconds.
echo If not, manually navigate to: http://localhost:3000
echo.
echo To stop the servers, close the server windows.
echo.
echo ============================================
echo.
pause