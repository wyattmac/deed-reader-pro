@echo off
echo ============================================
echo Running Pre-commit Hooks Manually...
echo ============================================

echo.
echo Checking if pre-commit is installed...
if not exist deed-reader-web\backend\venv\Scripts\pre-commit.exe (
    echo ERROR: Pre-commit not found!
    echo Please run SETUP_PRECOMMIT.bat first
    pause
    exit /b 1
)

echo.
echo Running pre-commit on all files...
deed-reader-web\backend\venv\Scripts\pre-commit run --all-files

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ All pre-commit hooks passed!
) else (
    echo.
    echo ❌ Some pre-commit hooks failed!
    echo Review the output above and fix any issues.
)

pause