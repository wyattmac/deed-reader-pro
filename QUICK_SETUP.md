# ⚡ Deed Reader Pro - Quick Setup Guide

## 🚀 First Time Setup (5 minutes)

### 1. Clone & Navigate
```bash
cd "dEED READ"
```

### 2. Run Test & Setup
```bash
scripts\TEST_APP.bat
# This installs all dependencies automatically
```

### 3. Configure API Key
- Edit: `deed-reader-web/backend/.env`
- Replace: `ANTHROPIC_API_KEY=sk-ant-api03-your-key-here`
- Save file

### 4. Start Application
```bash
scripts\RUN_APP.bat
# Choose Y to kill existing processes
```

### 5. Verify (30 seconds later)
```bash
curl http://localhost:5000/api/health
# Look for: "claude": "healthy"
```

**Frontend**: http://localhost:3000  
**Backend**: http://localhost:5000

---

## 🔧 Daily Development Workflow

### Starting Fresh
```bash
scripts\RUN_APP.bat
```

### After Code Changes
```bash
# Frontend changes: Auto-reloads
# Backend changes: Restart needed
scripts\RUN_APP.bat
```

### After Config Changes (.env, requirements.txt)
```bash
scripts\RUN_APP.bat  # Always restart!
```

### Making Commits
```bash
scripts\GIT_COMMIT.bat
```

### Troubleshooting
```bash
scripts\TROUBLESHOOT.bat
```

---

## ⚡ Pro Tips for Speed

### 🎯 **Key Rule**: Environment changes require restart
- ✅ Update `.env` → Restart immediately
- ✅ Change dependencies → Restart immediately  
- ❌ Don't test health endpoint with old backend running

### 🔧 **Use the Right Scripts**
- `RUN_APP.bat` - Main launcher (handles everything)
- `TEST_APP.bat` - Dependency check/install
- `RESTART.bat` - Quick restart (if working)

### 🚀 **Fastest Path to Working App**
1. `scripts\TEST_APP.bat` (first time only)
2. Edit `.env` with real API key
3. `scripts\RUN_APP.bat` 
4. ✅ Done!

### 🐛 **Quick Debug Checks**
```bash
# 1. Is backend running?
curl http://localhost:5000/api/health

# 2. Is Claude working?
# Look for: "claude": "healthy"

# 3. Frontend loading?
# Visit: http://localhost:3000
```

---

## 🚨 Common Gotchas

### ❌ **Don't Do This**
- Test API while old backend is running
- Forget to restart after `.env` changes
- Run `python app.py` from wrong directory
- Skip the virtual environment activation

### ✅ **Do This Instead**  
- Always use `scripts\RUN_APP.bat`
- Restart immediately after config changes
- Check health endpoint after each restart
- Trust the automation scripts

---

## 📁 **File Locations to Remember**

```
dEED READ/
├── scripts\RUN_APP.bat          # 🚀 Main launcher
├── scripts\TEST_APP.bat         # 🔧 Dependency installer  
└── deed-reader-web/
    ├── backend/.env             # 🔑 API key goes here
    ├── backend/requirements.txt # 📦 Python packages
    └── frontend/package.json    # 📦 Node packages
```

**Next time**: This whole process should take **2-3 minutes max**! 🎯 