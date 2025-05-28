# 🧹 Project Cleanup Guide

This guide explains how to clean build artifacts and dependencies from your Deed Reader Pro project.

## 🎯 Quick Cleanup

**Run the cleanup script:**
```bash
scripts/CLEAN_PROJECT.bat
```

This script safely removes all build artifacts and provides confirmations before deletion.

## 📋 What Gets Deleted

### **Large Dependencies (500MB-1GB+)**
- `deed-reader-web/frontend/node_modules/` - NPM packages
- `deed-reader-web/backend/venv/` - Python virtual environment

### **Build Artifacts**
- `deed-reader-web/frontend/build/` - React production build
- `**/__pycache__/` - Python bytecode cache
- `*.pyc`, `*.pyo` - Compiled Python files

### **Temporary Files**
- `deed-reader-web/backend/uploads/*.pdf` - Uploaded documents
- `deed-reader-web/backend/uploads/*.png` - Image uploads
- Log files and cache directories

## 🔄 How to Restore

After cleanup, restore everything by running:
```bash
scripts/RUN_APP.bat
```

This automatically:
1. Creates new Python virtual environment
2. Installs all Python dependencies
3. Installs all NPM packages
4. Starts the application

## 🛡️ What's Protected

These files are **NEVER** deleted:
- **Source code** (*.py, *.tsx, *.ts, *.js)
- **Configuration** (package.json, requirements.txt, .env)
- **Documentation** (*.md files)
- **Scripts** (*.bat files)
- **Templates** (.env.example, env.template)

## 🎯 Professional Benefits

### **Repository Management**
- **Smaller git repos** - Faster clones and operations
- **Clean commits** - No accidental dependency commits
- **Platform independence** - Works on any machine

### **Development Workflow**
- **Fresh builds** - Eliminates corruption and conflicts
- **Consistent environments** - Everyone builds from scratch
- **Faster transfers** - MB instead of GB for backups

## 📊 .gitignore Protection

The comprehensive `.gitignore` file prevents accidentally committing:

```gitignore
# Major exclusions
node_modules/          # NPM dependencies
venv/                  # Python virtual environment
build/                 # Build outputs
__pycache__/          # Python cache
*.log                 # Log files
.env                  # Environment variables
uploads/*.pdf         # Temporary uploads
```

## ⚡ Manual Cleanup Commands

If you prefer manual control:

```bash
# Frontend cleanup
rmdir /s /q deed-reader-web\frontend\node_modules
rmdir /s /q deed-reader-web\frontend\build

# Backend cleanup
rmdir /s /q deed-reader-web\backend\venv
for /d /r deed-reader-web\backend %i in (__pycache__) do rmdir /s /q "%i"

# Temp files
del /q deed-reader-web\backend\uploads\*.pdf
```

## 🔍 Verification

After cleanup, verify your project structure:

```bash
# Should exist (source code)
deed-reader-web/frontend/src/
deed-reader-web/backend/app.py
package.json
requirements.txt

# Should NOT exist (build artifacts)
deed-reader-web/frontend/node_modules/
deed-reader-web/backend/venv/
deed-reader-web/frontend/build/
```

## ⚠️ Important Notes

1. **Always commit source changes** before cleanup
2. **Ensure you have internet** for dependency reinstallation
3. **Close running servers** before cleanup to avoid file locks
4. **Backup `.env` files** if they contain important configurations

---

**💡 Pro Tip:** Run cleanup regularly to keep your project lean and professional!