@echo off
title EduPredict AI - Sapthagiri NPS University
cls
echo ==============================================================================
echo       SAPTHAGIRI NPS UNIVERSITY, BENGALURU - EduPredict AI DESKTOP APP
echo                 Department of Computer Science & Engineering
echo ==============================================================================
echo.
echo Choose your preferred App Mode:
echo   [1] Launch Native Python Desktop GUI Window (Tkinter)
echo   [2] Launch Full Web Dashboard in Dedicated Windows App Window (Edge App Mode)
echo   [3] Run Standard Web Browser Mode (http://localhost:8501)
echo   [4] Exit
echo.
set /p choice="Enter option (1, 2, or 3): "

if "%choice%"=="1" (
    echo Launching Native Desktop GUI Application...
    start pythonw desktop_app.py
    exit
)

if "%choice%"=="2" (
    echo Checking web service...
    start /min python -m streamlit run app.py --server.port 8501 --server.headless true
    timeout /t 2 >nul
    echo Launching dedicated Windows Desktop App window...
    start msedge.exe --app=http://localhost:8501 --window-size=1280,850
    exit
)

if "%choice%"=="3" (
    echo Starting Streamlit Web App...
    python -m streamlit run app.py
    pause
    exit
)

echo Exiting...
