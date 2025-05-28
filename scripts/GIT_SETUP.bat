@echo off
title Deed Reader Pro - GitHub Setup Helper
color 0B

echo ============================================
echo     DEED READER PRO - GITHUB SETUP
echo ============================================
echo.

:: Check if git is installed
echo [1/7] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/downloads
    echo Make sure to add Git to your PATH during installation.
    pause
    exit /b 1
)
echo [OK] Git is installed!

:: Check git configuration
echo.
echo [2/7] Checking Git user configuration...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo [SETUP NEEDED] Git user not configured.
    echo.
    set /p username="Enter your full name: "
    set /p email="Enter your email address: "
    
    git config --global user.name "!username!"
    git config --global user.email "!email!"
    git config --global init.defaultBranch main
    
    echo [OK] Git user configured successfully!
) else (
    echo [OK] Git user already configured:
    echo Name: 
    git config user.name
    echo Email: 
    git config user.email
)

:: Check if we're in a git repository
echo.
echo [3/7] Checking Git repository status...
cd /d "%~dp0\.."
git status >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Not in a Git repository!
    echo Please run this script from the project directory.
    pause
    exit /b 1
)
echo [OK] Git repository detected!

:: Show current status
echo.
echo [4/7] Current repository status:
git status --short

:: Check for remote
echo.
echo [5/7] Checking GitHub connection...
git remote -v 2>nul | findstr origin >nul
if errorlevel 1 (
    echo [SETUP NEEDED] No GitHub remote configured.
    echo.
    echo To connect to GitHub:
    echo 1. Create a repository on GitHub.com
    echo 2. Copy the repository URL
    echo 3. Run this command:
    echo.
    echo    git remote add origin https://github.com/USERNAME/REPOSITORY.git
    echo.
    echo Or use SSH:
    echo    git remote add origin git@github.com:USERNAME/REPOSITORY.git
    echo.
    goto :setup_complete
) else (
    echo [OK] GitHub remote configured:
    git remote -v
)

:: Test connection
echo.
echo [6/7] Testing GitHub connection...
git ls-remote origin >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Cannot connect to GitHub remote.
    echo This might be due to:
    echo - Authentication issues
    echo - Network connectivity
    echo - Repository doesn't exist
    echo.
    echo Please check your credentials and repository URL.
) else (
    echo [OK] GitHub connection successful!
)

:: Offer to make initial commit
echo.
echo [7/7] Initial commit setup...
git log --oneline -1 >nul 2>&1
if errorlevel 1 (
    echo [READY] No commits yet - ready for initial commit!
    echo.
    echo Would you like to make the initial commit now? (Y/N)
    choice /C YN /M "Your choice"
    if errorlevel 2 goto :setup_complete
    
    echo.
    echo Making initial commit...
    git add .
    git commit -m "Initial commit: Deed Reader Pro setup

🚀 Features:
- React TypeScript frontend with Tailwind CSS
- Flask Python backend with Claude AI integration  
- Professional project structure and organization
- Comprehensive linting and pre-commit hooks
- Complete documentation and setup guides
- Automated build and deployment scripts

🤖 Generated with Claude Code (https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

    if errorlevel 1 (
        echo [ERROR] Failed to create initial commit!
        goto :setup_complete
    )
    
    echo [OK] Initial commit created!
    
    :: Offer to push
    git remote -v 2>nul | findstr origin >nul
    if not errorlevel 1 (
        echo.
        echo Would you like to push to GitHub now? (Y/N)
        choice /C YN /M "Your choice"
        if errorlevel 2 goto :setup_complete
        
        echo.
        echo Pushing to GitHub...
        git push -u origin main
        
        if errorlevel 1 (
            echo [WARNING] Push failed! This might be due to:
            echo - Authentication issues
            echo - Repository doesn't exist on GitHub
            echo - Network connectivity
            echo.
            echo Please check the error above and try: git push -u origin main
        ) else (
            echo [OK] Successfully pushed to GitHub!
            echo.
            echo 🎉 Your project is now on GitHub!
        )
    )
) else (
    echo [OK] Repository already has commits:
    git log --oneline -3
)

:setup_complete
echo.
echo ============================================
echo     SETUP SUMMARY
echo ============================================
echo.
echo Git Status: [OK] Configured
echo Repository: [OK] Initialized  
echo GitHub Remote: 
git remote -v 2>nul | findstr origin >nul && echo [OK] Connected || echo [PENDING] Not configured
echo Commits: 
git log --oneline -1 >nul 2>&1 && echo [OK] Has commits || echo [PENDING] No commits yet
echo.
echo Next steps:
echo 1. If remote not configured: Connect to GitHub repository
echo 2. Use scripts\GIT_COMMIT.bat for easy commits
echo 3. See docs\GITHUB_SETUP.md for detailed instructions
echo.
pause