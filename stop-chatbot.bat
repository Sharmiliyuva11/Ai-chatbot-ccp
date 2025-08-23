@echo off
title AI Chatbot Stopper
color 0C
echo.
echo ===============================================
echo        🛑 AI CHATBOT STOPPER 🛑
echo ===============================================
echo.
echo Stopping all AI Chatbot processes...
echo.

echo Stopping Python (Backend)...
taskkill /F /IM python.exe /T 2>nul
if %errorlevel% equ 0 (
    echo ✅ Backend stopped successfully
) else (
    echo ⚠️ No Python processes found
)

echo.
echo Stopping Node.js (Frontend)...
taskkill /F /IM node.exe /T 2>nul
if %errorlevel% equ 0 (
    echo ✅ Frontend stopped successfully
) else (
    echo ⚠️ No Node.js processes found
)

echo.
echo ===============================================
echo   🎉 ALL PROCESSES STOPPED
echo ===============================================
echo.
timeout /t 3 /nobreak >nul