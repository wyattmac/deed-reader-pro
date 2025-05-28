@echo off
title Deed Reader Pro - Git Commit Helper
color 0B

echo ============================================
echo     DEED READER PRO - GIT COMMIT HELPER
echo ============================================
echo.

:: Navigate to project root
cd /d "%~dp0\.."

:: Check git status
echo [1/4] Checking repository status...
git status >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Not in a Git repository!
    echo Please run GIT_SETUP.bat first.
    pause
    exit /b 1
)

:: Show current changes
echo.
echo [2/4] Current changes:
echo ============================================
git status --short
echo ============================================
echo.

:: Check if there are any changes
git diff --quiet && git diff --cached --quiet
if not errorlevel 1 (
    echo [INFO] No changes to commit.
    echo.
    echo Current branch status:
    git status
    echo.
    pause
    exit /b 0
)

:: Show detailed diff (optional)
echo Would you like to see detailed changes? (Y/N)
choice /C YN /M "Your choice"
if errorlevel 1 if not errorlevel 2 (
    echo.
    echo Detailed changes:
    echo ============================================
    git diff --color=always
    echo ============================================
    echo.
)

:: Stage files
echo [3/4] Staging files...
echo.
echo Would you like to:
echo 1. Add all changes (git add .)
echo 2. Add specific files only
echo 3. Cancel
choice /C 123 /M "Your choice"

if errorlevel 3 goto :cancel
if errorlevel 2 goto :selective
if errorlevel 1 goto :add_all

:add_all
git add .
echo [OK] All changes staged!
goto :commit

:selective
echo.
echo Available files to stage:
git status --porcelain
echo.
set /p files="Enter files to add (space-separated): "
git add %files%
if errorlevel 1 (
    echo [ERROR] Failed to stage files!
    pause
    exit /b 1
)
echo [OK] Selected files staged!
goto :commit

:commit
:: Get commit message
echo.
echo [4/4] Creating commit...
echo.
echo Choose commit type:
echo 1. feat: New feature
echo 2. fix: Bug fix  
echo 3. docs: Documentation
echo 4. chore: Maintenance/tooling
echo 5. refactor: Code refactoring
echo 6. style: Code formatting
echo 7. test: Tests
echo 8. custom: Custom message
choice /C 12345678 /M "Your choice"

if errorlevel 8 goto :custom
if errorlevel 7 set "prefix=test: " && goto :get_message
if errorlevel 6 set "prefix=style: " && goto :get_message  
if errorlevel 5 set "prefix=refactor: " && goto :get_message
if errorlevel 4 set "prefix=chore: " && goto :get_message
if errorlevel 3 set "prefix=docs: " && goto :get_message
if errorlevel 2 set "prefix=fix: " && goto :get_message
if errorlevel 1 set "prefix=feat: " && goto :get_message

:get_message
echo.
set /p message="Enter commit message: "
set "full_message=%prefix%%message%"
goto :do_commit

:custom
echo.
set /p full_message="Enter full commit message: "
goto :do_commit

:do_commit
echo.
echo Commit message: %full_message%
echo.
echo Proceed with commit? (Y/N)
choice /C YN /M "Your choice"
if errorlevel 2 goto :cancel

:: Create commit
git commit -m "%full_message%

🤖 Generated with Claude Code (https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

if errorlevel 1 (
    echo [ERROR] Commit failed!
    echo.
    echo This might be due to:
    echo - Pre-commit hooks failing
    echo - No changes staged
    echo - Git configuration issues
    echo.
    pause
    exit /b 1
)

echo [OK] Commit created successfully!

:: Offer to push
echo.
echo Would you like to push to GitHub? (Y/N)
choice /C YN /M "Your choice"
if errorlevel 2 goto :complete

echo.
echo Pushing to GitHub...
git push

if errorlevel 1 (
    echo [WARNING] Push failed!
    echo.
    echo This might be due to:
    echo - Authentication issues
    echo - No remote repository configured
    echo - Network connectivity
    echo - Branch conflicts
    echo.
    echo You can try pushing manually with: git push
) else (
    echo [OK] Successfully pushed to GitHub!
)

goto :complete

:cancel
echo.
echo [CANCELLED] No commit made.
goto :complete

:complete
echo.
echo ============================================
echo     COMMIT SUMMARY
echo ============================================
echo.
echo Latest commits:
git log --oneline -3
echo.
echo Repository status:
git status --short
echo.
pause