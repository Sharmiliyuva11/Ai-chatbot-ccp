# AI Chatbot Startup Script (PowerShell)
Write-Host "===============================================" -ForegroundColor Green
Write-Host "        🤖 AI CHATBOT LAUNCHER 🤖" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

$backendPath = "c:\Users\Y.SHARMILI\OneDrive\Desktop\Ai chatbot ccp\ai-growth-chatbot\backend"
$frontendPath = "c:\Users\Y.SHARMILI\OneDrive\Desktop\Ai chatbot ccp\ai-growth-chatbot\frontend"

# Check if paths exist
if (-not (Test-Path $backendPath)) {
    Write-Host "❌ Backend path not found!" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $frontendPath)) {
    Write-Host "❌ Frontend path not found!" -ForegroundColor Red
    exit 1
}

Write-Host "1. Starting Backend Server..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; Write-Host 'Backend Starting...' -ForegroundColor Green; python app.py"

Start-Sleep -Seconds 5

Write-Host "2. Starting Frontend Server..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendPath'; Write-Host 'Frontend Starting...' -ForegroundColor Green; npm run dev"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "   🎉 BOTH SERVICES STARTING..." -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Backend will run on: http://localhost:5000" -ForegroundColor Green
Write-Host "✅ Frontend will run on: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Open your browser and go to:" -ForegroundColor Cyan
Write-Host "   http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "🔐 Demo Login:" -ForegroundColor Cyan
Write-Host "   Username: user" -ForegroundColor White
Write-Host "   Password: 123" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to close this launcher..."
Read-Host