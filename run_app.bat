@echo off
TITLE AI-Powered Expense & Invoice Automation System
echo =====================================================================
echo  AI-Powered Expense & Invoice Automation System - Startup Launcher
echo =====================================================================
echo.

REM Set project root in PYTHONPATH
set PYTHONPATH=%CD%

echo [1/3] Checking and clearing occupied ports (8501, 8000)...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-NetTCPConnection -LocalPort 8501 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"
timeout /t 1 /nobreak > nul

echo [2/3] Checking FastAPI Backend on http://127.0.0.1:8000 ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $res = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health' -TimeoutSec 2; if ($res.status -eq 'healthy') { exit 0 } else { exit 1 } } catch { exit 1 }"
if %ERRORLEVEL% EQU 0 (
    echo       FastAPI Backend is already active and healthy!
) else (
    echo       Starting FastAPI Backend server...
    start "ExpenseAI Backend (FastAPI)" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"
    timeout /t 2 /nobreak > nul
)

echo [3/3] Starting Streamlit Frontend on http://localhost:8501 ...
start "ExpenseAI Frontend (Streamlit)" cmd /k "python -m streamlit run frontend\app.py --server.port 8501"

echo.
echo =====================================================================
echo  Application is running!
echo  - Frontend Dashboard: http://localhost:8501
echo  - Backend API Docs:   http://127.0.0.1:8000/docs
echo =====================================================================
echo.
pause
