@echo off
echo ============================================
echo Running Backend Linting...
echo ============================================

cd deed-reader-web\backend

echo.
echo Activating virtual environment...
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo.
echo Running Python linting script...
python lint.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Linting errors found!
    echo.
    echo To automatically fix formatting:
    echo   black .
    echo   isort .
    exit /b 1
) else (
    echo.
    echo ✅ Backend linting passed!
)

pause