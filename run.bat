@echo off
REM Smart Clinic Management System - Windows Batch Runner
REM This script helps you run the application easily

echo.
echo ============================================================
echo Smart Clinic Management System - Launcher
echo ============================================================
echo.
echo Choose how to run the application:
echo.
echo 1. Web Interface (Recommended) - http://localhost:5000
echo 2. CLI Interface (Command Line) - Terminal-based
echo 3. Install/Update Dependencies
echo 4. Reset Database
echo 5. Exit
echo.

setlocal enabledelayedexpansion
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting web server...
    echo Open your browser: http://localhost:5000
    echo Press Ctrl+C to stop
    echo.
    python app.py
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Starting CLI...
    echo.
    python cli.py
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
    echo Done! All dependencies installed.
    goto prompt
)

if "%choice%"=="4" (
    echo.
    echo Resetting database...
    if exist clinic.db (
        del clinic.db
        echo Database deleted.
    )
    echo Database will be recreated on next run.
    goto prompt
)

if "%choice%"=="5" (
    echo Goodbye!
    goto end
)

echo Invalid choice. Please try again.
goto prompt

:prompt
pause
cls
goto start

:start
goto loop

:end
endlocal
