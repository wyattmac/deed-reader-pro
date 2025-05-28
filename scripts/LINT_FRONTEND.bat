@echo off
echo ============================================
echo Running Frontend Linting...
echo ============================================

cd deed-reader-web\frontend

echo.
echo Checking for ESLint...
call npm run lint

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Linting errors found!
    echo.
    echo To automatically fix some issues, run:
    echo npm run lint:fix
    exit /b 1
) else (
    echo.
    echo ✅ Frontend linting passed!
)

pause