@echo off
title Deed Reader Pro - Reset and Clean
color 0C

echo ============================================
echo   DEED READER PRO - RESET AND CLEAN
echo ============================================
echo.
echo WARNING: This will remove all dependencies and
echo reset the application to a clean state!
echo.
echo This is useful when:
echo - Dependencies are corrupted
echo - Versions are conflicting
echo - You want a fresh start
echo.
pause

echo.
echo [1/5] Killing any running processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/5] Removing backend virtual environment...
if exist "deed-reader-web\backend\venv" (
    rmdir /S /Q "deed-reader-web\backend\venv"
    echo Removed backend virtual environment
) else (
    echo No virtual environment found
)

echo [3/5] Removing frontend node_modules...
if exist "deed-reader-web\frontend\node_modules" (
    echo This may take a few minutes...
    rmdir /S /Q "deed-reader-web\frontend\node_modules" 2>nul
    echo Removed frontend node_modules
) else (
    echo No node_modules found
)

echo [4/5] Cleaning npm cache...
cd deed-reader-web\frontend
call npm cache clean --force >nul 2>&1
cd ..\..

echo [5/5] Removing temporary files...
if exist "deed-reader-web\backend\__pycache__" rmdir /S /Q "deed-reader-web\backend\__pycache__" 2>nul
if exist "deed-reader-web\frontend\package-lock.json" del /Q "deed-reader-web\frontend\package-lock.json" 2>nul

echo.
echo ============================================
echo   RESET COMPLETE
echo ============================================
echo.
echo The application has been reset to a clean state.
echo Run RUN_APP.bat to reinstall everything and start fresh.
echo.
pause