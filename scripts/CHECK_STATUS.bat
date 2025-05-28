@echo off
echo ============================================
echo   CHECKING APPLICATION STATUS
echo ============================================
echo.

echo [1] Checking Backend Status...
curl -s http://localhost:5000/api/health >nul 2>&1
if errorlevel 1 (
    echo    [FAIL] Backend is NOT running
    echo    Fix: Check the backend window for errors
) else (
    echo    [PASS] Backend is running!
    curl -s http://localhost:5000/api/health
)
echo.

echo [2] Checking Frontend Status...
curl -s http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    echo    [WAIT] Frontend might still be starting...
    echo    Note: Frontend takes 30-60 seconds to compile
    echo.
    echo    If it doesn't start after 2 minutes:
    echo    - Check the frontend window for errors
    echo    - Try opening http://localhost:3000 manually
) else (
    echo    [PASS] Frontend is responding!
)
echo.

echo [3] Quick Links:
echo    Backend API: http://localhost:5000/api/health
echo    Frontend UI: http://localhost:3000
echo.

pause