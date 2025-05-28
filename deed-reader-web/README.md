# Deed Reader Pro - Web Application

Modern web-based deed analysis powered by Anthropic Claude AI.

## 🏗️ Architecture

```
deed-reader-web/
├── frontend/                 # React TypeScript application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Main application pages
│   │   ├── services/       # API integration
│   │   └── App.tsx         # Main app component
│   └── package.json        # Frontend dependencies
├── backend/                 # Flask REST API
│   ├── app.py              # Main Flask application
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   │   ├── claude_service.py    # Claude AI integration
│   │   ├── ocr_service.py       # OCR processing
│   │   └── plotting_service.py  # Coordinate plotting
│   ├── core/               # Deed parsing algorithms
│   └── requirements.txt    # Python dependencies
└── SETUP_GUIDE.md          # Detailed setup instructions
```

## 🚀 Key Features

### AI-Powered Analysis
- **Claude-3.5 Sonnet** integration for intelligent document understanding
- **Vision API** for scanned document OCR
- **Confidence scoring** for extracted data
- **Natural language Q&A** about documents

### Document Processing
- **Multi-format support**: PDF, PNG, JPG, TIFF, TXT
- **Smart text extraction** with OCR fallback
- **Bearing/distance parsing** with multiple format support
- **Monument detection** and classification

### User Interface
- **Drag-and-drop** file upload
- **Real-time** processing feedback
- **Interactive results** display
- **Export capabilities** for processed data

## 🛠️ Technology Details

### Frontend Stack
- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **React Query** - Server state management
- **React Router v6** - Client-side routing
- **Axios** - HTTP client with interceptors

### Backend Stack
- **Flask 3.0** - Modern Python web framework
- **Anthropic Claude API** - AI document analysis
- **PyPDF2** - PDF text extraction
- **Pillow/OpenCV** - Image processing
- **python-dotenv** - Environment management

## 📡 API Endpoints

### Document Management
- `POST /api/documents/upload` - Upload deed files
- `POST /api/documents/text` - Process raw text
- `POST /api/documents/validate` - Validate document

### Analysis
- `POST /api/analysis/analyze` - Full AI analysis
- `POST /api/analysis/coordinates` - Extract coordinates
- `POST /api/analysis/summary` - Generate summary

### Chat Interface
- `POST /api/chat/ask` - Ask questions about document
- `GET /api/chat/history/{session_id}` - Get chat history
- `POST /api/chat/suggestions` - Get question suggestions

### Plotting
- `POST /api/plotting/plot` - Generate property plot
- `POST /api/plotting/closure` - Calculate closure
- `POST /api/plotting/export/{format}` - Export plot data

## 🔧 Configuration

### Required Environment Variables
```env
# backend/.env
ANTHROPIC_API_KEY=your-api-key-here
SECRET_KEY=your-secret-key
FLASK_DEBUG=true
UPLOAD_FOLDER=./uploads
```

### Frontend Configuration
```env
# frontend/.env
REACT_APP_API_URL=http://localhost:5000/api
```

## 🚀 Development

### Quick Start
Use the `RUN_APP.bat` script in the parent directory for automatic setup.

### Manual Development
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

## 📊 Data Flow

1. **Upload** → File validation → Text extraction
2. **Analysis** → Claude AI processing → Structured data
3. **Results** → Interactive display → Export options
4. **Q&A** → Context-aware responses → Chat history

## 🔒 Security Features

- API key management via environment variables
- File type validation and size limits
- CORS configuration for API access
- Secure file handling with cleanup
- Request logging and error tracking

## 🧪 Testing

Run backend tests:
```bash
cd backend
python test_api.py
python test_text_processing.py
```

## 📝 Notes

- Claude-3.5 Sonnet provides superior deed analysis
- OCR via Claude Vision API for scanned documents
- Automatic dependency installation via RUN_APP.bat
- Comprehensive error handling and user feedback