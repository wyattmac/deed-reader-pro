@echo off
echo ============================================
echo Running All Linting Checks...
echo ============================================

echo.
echo [1/2] Frontend Linting...
echo ============================================
call LINT_FRONTEND.bat

if %ERRORLEVEL% NEQ 0 (
    echo Frontend linting failed!
    set FRONTEND_FAILED=1
) else (
    set FRONTEND_FAILED=0
)

echo.
echo [2/2] Backend Linting...
echo ============================================
call LINT_BACKEND.bat

if %ERRORLEVEL% NEQ 0 (
    echo Backend linting failed!
    set BACKEND_FAILED=1
) else (
    set BACKEND_FAILED=0
)

echo.
echo ============================================
echo Summary:
echo ============================================

if %FRONTEND_FAILED%==0 (
    echo ✅ Frontend: PASSED
) else (
    echo ❌ Frontend: FAILED
)

if %BACKEND_FAILED%==0 (
    echo ✅ Backend: PASSED
) else (
    echo ❌ Backend: FAILED
)

echo.
if %FRONTEND_FAILED%==0 if %BACKEND_FAILED%==0 (
    echo 🎉 All linting checks passed!
    exit /b 0
) else (
    echo ❌ Some linting checks failed. Please fix the issues above.
    exit /b 1
)

pause