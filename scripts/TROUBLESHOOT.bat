@echo off
title Deed Reader Pro - Troubleshooter
color 0E

echo ============================================
echo   DEED READER PRO - TROUBLESHOOTER
echo ============================================
echo.

echo Running diagnostic checks...
echo.

:: Check Python
echo [CHECK] Python Installation:
python --version 2>nul
if errorlevel 1 (
    echo [FAIL] Python not found in PATH
    echo FIX: Install Python from https://python.org/downloads/
    echo      Make sure to check "Add Python to PATH"
) else (
    echo [PASS] Python is installed
)
echo.

:: Check Node.js
echo [CHECK] Node.js Installation:
node --version 2>nul
if errorlevel 1 (
    echo [FAIL] Node.js not found in PATH
    echo FIX: Install Node.js from https://nodejs.org/
) else (
    echo [PASS] Node.js is installed
)
echo.

:: Check npm
echo [CHECK] NPM Installation:
npm --version 2>nul
if errorlevel 1 (
    echo [FAIL] NPM not found
    echo FIX: Reinstall Node.js
) else (
    echo [PASS] NPM is installed
)
echo.

:: Check backend virtual environment
echo [CHECK] Backend Virtual Environment:
if exist "deed-reader-web\backend\venv" (
    echo [PASS] Virtual environment exists
) else (
    echo [FAIL] Virtual environment missing
    echo FIX: Run RUN_APP.bat to create it automatically
)
echo.

:: Check backend dependencies
echo [CHECK] Backend Dependencies:
if exist "deed-reader-web\backend\venv" (
    cd deed-reader-web\backend
    call venv\Scripts\activate.bat >nul 2>&1
    python -c "import flask, anthropic, PyPDF2" 2>nul
    if errorlevel 1 (
        echo [FAIL] Some backend dependencies missing
        echo FIX: Run RUN_APP.bat to install automatically
    ) else (
        echo [PASS] Core backend dependencies installed
    )
    cd ..\..
) else (
    echo [SKIP] Cannot check - virtual environment missing
)
echo.

:: Check frontend dependencies
echo [CHECK] Frontend Dependencies:
if exist "deed-reader-web\frontend\node_modules" (
    echo [PASS] Frontend dependencies installed
) else (
    echo [FAIL] Frontend dependencies missing
    echo FIX: Run RUN_APP.bat to install automatically
)
echo.

:: Check .env file
echo [CHECK] Backend Configuration (.env):
if exist "deed-reader-web\backend\.env" (
    cd deed-reader-web\backend
    findstr /C:"ANTHROPIC_API_KEY" .env >nul
    if errorlevel 1 (
        echo [FAIL] ANTHROPIC_API_KEY not found in .env
        echo FIX: Add your Anthropic API key to deed-reader-web\backend\.env
    ) else (
        findstr /C:"ANTHROPIC_API_KEY=your-anthropic-api-key-here" .env >nul
        if not errorlevel 1 (
            echo [WARN] ANTHROPIC_API_KEY is still the placeholder value
            echo FIX: Replace with your actual API key from https://console.anthropic.com/
        ) else (
            echo [PASS] ANTHROPIC_API_KEY is configured
        )
    )
    cd ..\..
) else (
    echo [FAIL] .env file not found
    echo FIX: Copy deed-reader-web\backend\env.template to .env and add your API key
)
echo.

:: Check ports
echo [CHECK] Port Availability:
netstat -an | findstr :5000 | findstr LISTENING >nul 2>&1
if not errorlevel 1 (
    echo [WARN] Port 5000 is in use (Backend)
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
        echo       PID: %%a
    )
)

netstat -an | findstr :3000 | findstr LISTENING >nul 2>&1
if not errorlevel 1 (
    echo [WARN] Port 3000 is in use (Frontend)
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
        echo       PID: %%a
    )
)

if errorlevel 1 (
    netstat -an | findstr :5000 | findstr LISTENING >nul 2>&1
    if errorlevel 1 (
        echo [PASS] Ports 3000 and 5000 are available
    )
)
echo.

:: Test backend health if running
echo [CHECK] Backend Health (if running):
curl -s http://localhost:5000/api/health >nul 2>&1
if not errorlevel 1 (
    echo [PASS] Backend is responding
) else (
    echo [INFO] Backend is not running
)
echo.

echo ============================================
echo   TROUBLESHOOTING COMPLETE
echo ============================================
echo.
echo If all checks pass, run RUN_APP.bat to start the application.
echo If issues persist, check the specific error messages above.
echo.
pause