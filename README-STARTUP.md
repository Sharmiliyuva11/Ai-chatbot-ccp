# 🤖 AI Chatbot - How to Run Every Time

## 🚀 Quick Start (Easiest Method)

**Double-click any of these files:**
- `start-chatbot.bat` - Starts both backend and frontend (Windows batch)
- `start-chatbot.ps1` - PowerShell version (more features)

## 🔧 Manual Method

### Step 1: Start Backend
```powershell
cd "c:\Users\Y.SHARMILI\OneDrive\Desktop\Ai chatbot ccp\ai-growth-chatbot\backend"
python app.py
```

### Step 2: Start Frontend (in new terminal)
```powershell
cd "c:\Users\Y.SHARMILI\OneDrive\Desktop\Ai chatbot ccp\ai-growth-chatbot\frontend"
npm run dev
```

## 🌐 Access Your Application

**URL:** `http://localhost:5173`

**Demo Credentials:**
- **Username:** `user`
- **Password:** `123`

## 🛑 How to Stop

**Option 1:** Double-click `stop-chatbot.bat`

**Option 2:** Manual - Close both terminal windows

**Option 3:** Manual - Press `Ctrl+C` in each terminal

## 📋 Startup Order

1. **Backend first** (port 5000) - API server
2. **Frontend second** (port 5173) - Web interface
3. **Access via browser** - Open http://localhost:5173

## 🚨 Troubleshooting

### Port Already in Use
```powershell
# Stop all processes
./stop-chatbot.bat
# Then restart
./start-chatbot.bat
```

### Backend Not Starting
- Check Python is installed
- Check you're in the correct directory
- Ensure dependencies are installed: `pip install -r requirements.txt`

### Frontend Not Starting
- Check Node.js is installed
- Check npm dependencies: `npm install`
- Ensure you're in the frontend directory

### Login Issues
- Verify backend is running (check http://localhost:5000)
- Use correct credentials: `user` / `123`
- Check browser console for errors

## 💡 Tips

- Always start backend before frontend
- Keep both terminals open while using the app
- The app uses in-memory storage (data resets on restart)
- MongoDB connection issues are normal - app works with memory storage

## 📁 File Locations

- **Main Project:** `c:\Users\Y.SHARMILI\OneDrive\Desktop\Ai chatbot ccp\`
- **Backend:** `ai-growth-chatbot\backend\`
- **Frontend:** `ai-growth-chatbot\frontend\`
- **Startup Scripts:** Root directory