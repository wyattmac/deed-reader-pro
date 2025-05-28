@echo off
echo ============================================
echo   RESTARTING DEED READER PRO
echo ============================================
echo.

echo [1/3] Stopping existing servers...
taskkill /F /FI "WINDOWTITLE eq Deed Reader Backend*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Deed Reader Frontend*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq dEED READ Backend*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq dEED READ Frontend*" >nul 2>&1

:: Also kill by port to be sure
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [2/3] Waiting for ports to clear...
timeout /t 3 /nobreak >nul

echo [3/3] Starting fresh instances...
call RUN_APP.bat

exit