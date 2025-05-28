# 🏠 Deed Reader Pro - AI-Powered Document Analysis

A powerful, AI-powered deed document analysis application for surveyors and real estate professionals, featuring Anthropic Claude integration for intelligent document processing.

## 🚀 Quick Start

**Windows Users:** Just double-click `RUN_APP.bat` - it handles everything automatically!

## ✨ Features

- **🤖 Claude AI Integration**: Advanced document analysis using Claude-3.5 Sonnet
- **📄 Multi-Format Support**: Process PDFs, images, and text files
- **🎯 Smart Extraction**: Automatically extract parties, descriptions, metes & bounds
- **💬 Interactive Q&A**: Ask questions about your documents in natural language
- **📊 Professional Results**: Structured output with confidence scores
- **🌐 Modern Web Interface**: React + TypeScript frontend

## 🛠️ Technology Stack

- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Flask REST API (Python 3.9+)
- **AI Engine**: Anthropic Claude-3.5 Sonnet
- **Document Processing**: PyPDF2, Pillow, OCR capabilities

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## 🔧 Installation

### Automatic Setup (Recommended)

1. Clone this repository
2. Get your Anthropic API key from [console.anthropic.com](https://console.anthropic.com/)
3. Double-click `RUN_APP.bat`
4. When prompted, add your API key to the `.env` file

The script will:
- ✅ Check all prerequisites
- ✅ Install dependencies automatically
- ✅ Start both servers
- ✅ Open your browser

### Manual Setup

See [SETUP_GUIDE.md](deed-reader-web/SETUP_GUIDE.md) for detailed manual installation steps.

## 📖 Usage

1. **Upload**: Drag and drop your deed document
2. **Analyze**: AI automatically extracts key information
3. **Review**: See structured results with:
   - Parties (grantor/grantee)
   - Property descriptions
   - Metes and bounds
   - Monuments and markers
   - Legal descriptions
4. **Ask Questions**: Use the chat interface for clarifications
5. **Export**: Download results in various formats

## 🚀 Utility Scripts

- **`RUN_APP.bat`** - Smart launcher that handles everything
- **`TROUBLESHOOT.bat`** - Diagnose and fix common issues
- **`CHECK_STATUS.bat`** - Verify servers are running
- **`RESET_AND_CLEAN.bat`** - Fresh start if needed

## 🔍 Troubleshooting

### Common Issues

**"localhost refused to connect"**
- Run `RUN_APP.bat` - it installs dependencies automatically

**"Module not found" errors**
- The app will auto-install missing packages on startup

**API Key Issues**
- Add your Anthropic API key to `deed-reader-web/backend/.env`
- Get a key from https://console.anthropic.com/

### Need Help?

1. Run `TROUBLESHOOT.bat` for automatic diagnostics
2. Check `QUICK_START.txt` for common fixes
3. See [SETUP_GUIDE.md](deed-reader-web/SETUP_GUIDE.md) for detailed help

## 📁 Project Structure

```
dEED READ/
├── RUN_APP.bat              # 🚀 Smart launcher (start here!)
├── TROUBLESHOOT.bat         # 🔧 Diagnostic tool
├── CHECK_STATUS.bat         # 📊 Status checker
├── QUICK_START.txt          # 📖 Quick reference
├── deed-reader-web/
│   ├── backend/            # Flask API + Claude integration
│   ├── frontend/           # React TypeScript app
│   └── SETUP_GUIDE.md      # Detailed setup instructions
└── README.md               # This file
```

## 🔒 Security

- API keys are stored in `.env` files (not committed to git)
- `.gitignore` configured to protect sensitive data
- CORS configured for local development

## 🤝 Contributing

This is a professional tool for deed analysis. Contributions that improve accuracy, performance, or usability are welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines including:
- Branch naming conventions (`feature/thing-you're-building`)
- Code standards and folder structure
- Development workflow and testing requirements

## 📄 License

Private project - All rights reserved

---

**Built with ❤️ for surveyors and real estate professionals**