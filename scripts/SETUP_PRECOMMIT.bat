@echo off
echo ============================================
echo Setting up Pre-commit Hooks...
echo ============================================

echo.
echo Installing pre-commit in backend virtual environment...
cd deed-reader-web\backend

if exist venv\Scripts\activate (
    call venv\Scripts\activate
    pip install pre-commit==3.6.0
) else (
    echo ERROR: Backend virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo.
echo Going back to project root...
cd ..\..

echo.
echo Installing pre-commit hooks...
deed-reader-web\backend\venv\Scripts\pre-commit install

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Pre-commit hooks installed successfully!
    echo.
    echo The hooks will now run automatically before each commit.
    echo.
    echo To manually run hooks on all files:
    echo   deed-reader-web\backend\venv\Scripts\pre-commit run --all-files
    echo.
    echo To skip hooks for a commit (not recommended):
    echo   git commit --no-verify
) else (
    echo.
    echo ❌ Failed to install pre-commit hooks!
    exit /b 1
)

pause