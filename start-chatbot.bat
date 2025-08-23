@echo off
title AI Chatbot Launcher
color 0A
echo.
echo ===============================================
echo        🤖 AI CHATBOT LAUNCHER 🤖
echo ===============================================
echo.
echo Starting both Backend and Frontend...
echo.
echo 1. Starting Backend Server...
start "AI Chatbot Backend" cmd /k "cd /d ""c:\Users\Y.SHARMILI\OneDrive\Desktop\Ai chatbot ccp\ai-growth-chatbot\backend"" && echo Starting Backend... && python app.py"

timeout /t 5 /nobreak >nul

echo 2. Starting Frontend Server...
start "AI Chatbot Frontend" cmd /k "cd /d ""c:\Users\Y.SHARMILI\OneDrive\Desktop\Ai chatbot ccp\ai-growth-chatbot\frontend"" && echo Starting Frontend... && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ===============================================
echo   🎉 BOTH SERVICES STARTING...
echo ===============================================
echo.
echo ✅ Backend will run on: http://localhost:5000
echo ✅ Frontend will run on: http://localhost:5173
echo.
echo 🌐 Open your browser and go to:
echo    http://localhost:5173
echo.
echo 🔐 Demo Login:
echo    Username: user
echo    Password: 123
echo.
echo Press any key to close this launcher...
pause >nul