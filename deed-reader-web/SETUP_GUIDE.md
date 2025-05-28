# 🚀 Deed Reader Pro - Setup Guide

Complete setup instructions for the Claude-powered deed analysis application.

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.9+** ([Download](https://www.python.org/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Anthropic API Key** ([Get one here](https://console.anthropic.com/))

## 🎯 Quick Start (Recommended)

The easiest way to get started:

1. **Get your API key** from [console.anthropic.com](https://console.anthropic.com/)
2. **Double-click** `RUN_APP.bat` in the root directory
3. **Add your API key** when prompted

That's it! The smart launcher handles everything else automatically.

## 🔧 Manual Setup

If you prefer manual setup or are on Mac/Linux:

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd deed-reader-web/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Configure environment:**
   ```bash
   # Copy template
   cp env.template .env
   
   # Edit .env and add your Anthropic API key
   ANTHROPIC_API_KEY=your-actual-api-key-here
   ```

6. **Start backend server:**
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd deed-reader-web/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

## 🔧 Configuration

### Backend Configuration (.env)

```env
# Required
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Optional
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=true
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=52428800  # 50MB
```

### Frontend Configuration

The frontend automatically connects to `http://localhost:5000` during development.

For production, create `.env.production`:
```env
REACT_APP_API_URL=https://your-api-domain.com/api
```

## 🚀 Running the Application

### Using Utility Scripts (Windows)

- **`RUN_APP.bat`** - Checks dependencies and starts everything
- **`CHECK_STATUS.bat`** - Verify both servers are running
- **`TROUBLESHOOT.bat`** - Diagnose common issues

### Manual Start

1. **Backend** (Terminal 1):
   ```bash
   cd deed-reader-web/backend
   venv\Scripts\activate  # or source venv/bin/activate
   python app.py
   ```

2. **Frontend** (Terminal 2):
   ```bash
   cd deed-reader-web/frontend
   npm start
   ```

3. **Access the app** at http://localhost:3000

## 🔍 Verifying Installation

1. **Backend health check:**
   ```bash
   curl http://localhost:5000/api/health
   ```
   Should return: `{"status": "healthy", ...}`

2. **Frontend:** Should automatically open in browser

3. **Test upload:** Try uploading a sample deed document

## 🚨 Troubleshooting

### Common Issues

**Port already in use:**
- Windows: `RUN_APP.bat` will offer to kill the process
- Manual: Find and kill the process using the port

**Module not found errors:**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

**API key not working:**
- Verify key at [console.anthropic.com](https://console.anthropic.com/)
- Check for typos or extra spaces
- Ensure you have available credits

**CORS errors:**
- Backend must be running on port 5000
- Frontend must be on port 3000
- Check `CORS_ORIGINS` in backend `.env`

### Reset Everything

If all else fails:
```bash
# Windows
RESET_AND_CLEAN.bat
RUN_APP.bat

# Manual
rm -rf deed-reader-web/backend/venv
rm -rf deed-reader-web/frontend/node_modules
# Then follow setup steps again
```

## 📊 Supported File Types

- **Text**: `.txt`
- **PDF**: `.pdf` (with text or scanned)
- **Images**: `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`

## 🔒 Security Notes

- Never commit `.env` files to version control
- Keep your API keys secure
- Use environment variables for sensitive data
- Enable HTTPS in production

## 🎯 Next Steps

1. Upload a deed document
2. Review the AI analysis
3. Try the chat interface
4. Export results as needed

## 📚 Additional Resources

- [Main README](../README.md)
- [API Documentation](README.md)
- [Anthropic Documentation](https://docs.anthropic.com/)

---

**Need help?** Run `TROUBLESHOOT.bat` for automatic diagnostics!