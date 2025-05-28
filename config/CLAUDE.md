# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Deed Reader Pro is a modern web application for analyzing deed documents using AI. It consists of:
- **Frontend**: React 18 + TypeScript + Tailwind CSS (port 3000)
- **Backend**: Flask REST API with Anthropic Claude integration (port 5000)

The application extracts structured data from deed documents including parties, property descriptions, metes and bounds, monuments, and legal descriptions using Claude-3.5 Sonnet AI.

## Essential Commands

### Quick Start (Windows)
```bash
# Start both servers automatically with dependency checks
RUN_APP.bat

# Troubleshoot issues
TROUBLESHOOT.bat

# Check server status
CHECK_STATUS.bat

# Run linting checks
LINT_ALL.bat          # Lint both frontend and backend
LINT_FRONTEND.bat     # Lint frontend only
LINT_BACKEND.bat      # Lint backend only

# Pre-commit hooks
SETUP_PRECOMMIT.bat   # Install pre-commit hooks
RUN_PRECOMMIT.bat     # Run pre-commit hooks manually
```

### Backend Commands
```bash
cd deed-reader-web/backend
python -m venv venv
venv\Scripts\activate              # Windows
source venv/bin/activate           # macOS/Linux
pip install -r requirements.txt
python app.py

# Run tests
python test_api.py
python test_openai.py
python test_text_processing.py
python test_tiny_rd_deed.py

# Run linting
python lint.py                     # Run all linting checks
flake8 .                          # Style guide checking
black .                           # Auto-format code
isort .                           # Sort imports

# Pre-commit hooks
pre-commit install                 # Install hooks
pre-commit run --all-files         # Run hooks manually
```

### Frontend Commands
```bash
cd deed-reader-web/frontend
npm install
npm start                          # Development server
npm run build                      # Production build
npm test                           # Run tests
npm run lint                       # Run ESLint
npm run lint:fix                   # Auto-fix ESLint issues
```

## Architecture & Key Components

### Backend Structure
- **app.py**: Main Flask application with route configuration and CORS setup
- **routes/**: API endpoints
  - `document_routes.py`: File upload and document processing
  - `analysis_routes.py`: AI-powered deed analysis
  - `chat_routes.py`: Q&A functionality
  - `plotting_routes.py`: Property boundary visualization
- **services/**: 
  - `claude_service.py`: Anthropic Claude API integration (primary AI service)
  - `openai_service.py`: Legacy OpenAI integration
  - `ocr_service.py`: OCR for scanned documents
  - `plotting_service.py`: Coordinate plotting
- **core/**: Deed parsing logic
  - `deed_parser.py`: Advanced pattern matching for bearings, distances, monuments
  - `bearing_parser.py`: Converts various bearing formats
  - `deed_text_filter.py`: Text preprocessing
  - `advanced_deed_filter.py`: Enhanced filtering

### Frontend Structure
- **pages/**: Main application views
  - `HomePage.tsx`: Landing page with upload
  - `AnalysisPage.tsx`: Document analysis results
  - `ChatPage.tsx`: Interactive Q&A
  - `PlottingPage.tsx`: Property visualization
- **components/**: Reusable UI components
- **services/api.ts**: Axios-based API client with type safety

### Key Features Implementation
1. **File Upload**: React Dropzone → Flask → PDF/Image processing
2. **AI Analysis**: Document → Claude API → Structured JSON response
3. **Coordinate Extraction**: Regex patterns → Bearing/distance parsing → Plot data
4. **Chat Interface**: Natural language queries → Claude API → Contextual answers

## Environment Configuration

Required in `deed-reader-web/backend/.env`:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

The application uses Anthropic Claude-3.5 Sonnet (model: claude-3-5-sonnet-20241022) for superior deed parsing accuracy.

## API Endpoints

- `POST /api/documents/upload` - Upload deed document
- `POST /api/documents/analyze` - Analyze uploaded document
- `POST /api/chat` - Ask questions about document
- `GET /api/health` - Health check

## Development Notes

- Frontend proxies API requests to localhost:5000 during development
- Backend uses Flask debug mode with auto-reload
- Frontend uses React hot-reload
- File uploads stored in `backend/uploads/`
- Maximum file size: 50MB

## Branch Naming Conventions

Follow these patterns for consistent git workflow:

- `feature/thing-you're-building` - New functionality
- `bugfix/issue-description` - Bug fixes
- `hotfix/critical-fix` - Production critical fixes
- `chore/maintenance-task` - Dependencies, tooling
- `docs/documentation-update` - Documentation changes

Examples:
- `feature/claude-vision-integration`
- `bugfix/pdf-upload-validation`
- `chore/update-dependencies`

## Code Quality & Pre-commit Hooks

Pre-commit hooks automatically run linting and formatting before each commit:

**Setup (one-time):**
```bash
SETUP_PRECOMMIT.bat    # Windows
# OR manually:
cd deed-reader-web/backend
pip install pre-commit
cd ../..
pre-commit install
```

**What runs automatically:**
- Python: black (formatting), isort (imports), flake8 (linting)
- Frontend: ESLint (linting)
- General: trailing whitespace, file endings, YAML validation

**Manual execution:**
```bash
RUN_PRECOMMIT.bat           # Windows
pre-commit run --all-files  # All files
```

**Skip hooks (not recommended):**
```bash
git commit --no-verify
```

## Testing Approach

- Backend: Direct Python test scripts in backend root
- Frontend: Jest tests via `npm test`
- No automated linting or formatting currently configured