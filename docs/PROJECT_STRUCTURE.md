# 📁 Project Structure

This document outlines the complete folder structure and organization of Deed Reader Pro.

## 🏗️ Root Directory

```
dEED READ/
├── 📄 README.md                    # Main project documentation
├── 📄 CONTRIBUTING.md              # Development guidelines
├── 📄 PROJECT_STRUCTURE.md         # This file
├── 📄 CLAUDE.md                    # Claude Code instructions
├── 📄 ENHANCEMENT_PLAN.md          # Future improvements
├── 📄 QUICK_START.txt              # Quick reference guide
├── 🔧 .pre-commit-config.yaml      # Pre-commit hooks configuration
├── 🔧 .gitignore                   # Git ignore patterns
│
├── 🚀 RUN_APP.bat                  # Quick launcher (Windows)
├── 🔧 TROUBLESHOOT.bat             # Diagnostic tool
├── 📊 CHECK_STATUS.bat             # Server status checker
├── 🧹 RESET_AND_CLEAN.bat          # Clean restart utility
├── 🧪 LINT_ALL.bat                 # Comprehensive linting
├── 🧪 LINT_FRONTEND.bat            # Frontend linting only
├── 🧪 LINT_BACKEND.bat             # Backend linting only
├── 🔧 SETUP_PRECOMMIT.bat          # Pre-commit hooks installer
├── 🔧 RUN_PRECOMMIT.bat            # Manual pre-commit execution
│
├── 🗂️ deed-reader-web/             # Main application directory
└── 📄 sample_simple_deed.txt       # Sample data for testing
```

## 🌐 Web Application Structure

```
deed-reader-web/
├── 📄 README.md                    # Web app overview
├── 📄 SETUP_GUIDE.md               # Detailed setup instructions
│
├── 🖥️ frontend/                    # React TypeScript application
│   ├── 📄 README.md                # Frontend-specific docs
│   ├── 📄 package.json             # Dependencies and scripts
│   ├── 📄 package-lock.json        # Locked dependency versions
│   ├── 📄 tsconfig.json            # TypeScript configuration
│   ├── 📄 tailwind.config.js       # Tailwind CSS config
│   ├── 🔧 .eslintrc.json           # ESLint configuration
│   ├── 🔧 .env.example             # Environment variables template
│   │
│   ├── 📁 public/                  # Static assets
│   │   ├── index.html              # HTML template
│   │   └── manifest.json           # PWA manifest
│   │
│   ├── 📁 src/                     # Source code
│   │   ├── 📄 index.tsx            # Application entry point
│   │   ├── 📄 App.tsx              # Root component
│   │   ├── 📄 App.css              # Global styles
│   │   ├── 📄 index.css            # Base styles
│   │   │
│   │   ├── 🗂️ components/          # Reusable UI components
│   │   │   ├── UI/                 # Generic components
│   │   │   ├── Forms/              # Form components
│   │   │   ├── Layout/             # Layout components
│   │   │   │   ├── Header.tsx      # Application header
│   │   │   │   └── Sidebar.tsx     # Navigation sidebar
│   │   │   └── Plot/               # Plotting components
│   │   │       ├── ClosureReport.tsx
│   │   │       ├── ExportMenu.tsx
│   │   │       └── InteractivePlot.tsx
│   │   │
│   │   ├── 📁 pages/               # Route-level components
│   │   │   ├── HomePage.tsx        # Landing page
│   │   │   ├── AnalysisPage.tsx    # Document analysis
│   │   │   ├── ChatPage.tsx        # AI chat interface
│   │   │   ├── PlottingPage.tsx    # Property visualization
│   │   │   └── SettingsPage.tsx    # Application settings
│   │   │
│   │   ├── 🔧 services/            # External integrations
│   │   │   └── api.ts              # API client configuration
│   │   │
│   │   ├── 🛠️ utils/               # Utility functions
│   │   │   ├── index.ts            # Utility exports
│   │   │   ├── formatters.ts       # Data formatting
│   │   │   ├── validators.ts       # Input validation
│   │   │   └── api-helpers.ts      # API utilities
│   │   │
│   │   ├── 🎣 hooks/               # Custom React hooks
│   │   │   ├── index.ts            # Hook exports
│   │   │   ├── useDebounce.ts      # Debouncing hook
│   │   │   └── useLocalStorage.ts  # localStorage hook
│   │   │
│   │   ├── 📝 types/               # TypeScript definitions
│   │   │   └── index.ts            # Type exports
│   │   │
│   │   └── 📊 constants/           # Application constants
│   │       └── index.ts            # Constant exports
│   │
│   ├── 📁 build/                   # Production build output
│   └── 📁 node_modules/            # Dependencies (auto-generated)
│
└── 🐍 backend/                     # Flask Python API
    ├── 📄 app.py                   # Main Flask application
    ├── 📄 config.py                # Application configuration
    ├── 📄 requirements.txt         # Python dependencies
    ├── 🔧 .env.example             # Environment template
    ├── 🔧 .flake8                  # Python linting config
    ├── 🔧 pyproject.toml           # Python project config
    ├── 🧪 lint.py                  # Python linting script
    │
    ├── 🗂️ routes/                  # API endpoint handlers
    │   ├── analysis_routes.py      # Document analysis endpoints
    │   ├── chat_routes.py          # Chat interface endpoints
    │   ├── document_routes.py      # File upload endpoints
    │   └── plotting_routes.py      # Visualization endpoints
    │
    ├── 🔧 services/                # Business logic layer
    │   ├── claude_service.py       # Anthropic Claude integration
    │   ├── ocr_service.py          # OCR processing
    │   ├── ocr_fallback_service.py # OCR fallback methods
    │   └── plotting_service.py     # Coordinate plotting
    │
    ├── 🧠 core/                    # Core processing algorithms
    │   ├── __init__.py             # Package initialization
    │   ├── deed_parser.py          # Main parsing logic
    │   ├── bearing_parser.py       # Bearing/direction parsing
    │   ├── deed_text_filter.py     # Text preprocessing
    │   └── advanced_deed_filter.py # Enhanced filtering
    │
    ├── 🧪 tests/                   # Test files
    │   ├── test_api.py             # API endpoint tests
    │   ├── test_text_processing.py # Text processing tests
    │   └── test_tiny_rd_deed.py    # Specific deed tests
    │
    ├── 📁 uploads/                 # Temporary file storage
    └── 📁 venv/                    # Python virtual environment
```

## 🎯 Key Design Principles

### Frontend Organization
- **Components**: Organized by function (UI, Forms, Layout, Plot)
- **Pages**: Route-level components for major application sections
- **Services**: External API interactions and data fetching
- **Utils**: Pure functions for data manipulation and validation
- **Hooks**: Reusable stateful logic
- **Types**: Centralized TypeScript type definitions
- **Constants**: Application-wide constants and configuration

### Backend Organization
- **Routes**: API endpoint definitions and request handling
- **Services**: Business logic and external service integrations
- **Core**: Document parsing and analysis algorithms
- **Config**: Environment and application configuration
- **Tests**: Comprehensive test coverage

### File Naming Conventions
- **React Components**: PascalCase (`HomePage.tsx`)
- **Utilities**: camelCase (`formatters.ts`)
- **Python Files**: snake_case (`claude_service.py`)
- **Configuration**: lowercase with dots (`.eslintrc.json`)

### Import/Export Patterns
- **Barrel Exports**: Use `index.ts` files for clean imports
- **Named Exports**: Prefer named exports over default exports
- **Type-Only Imports**: Use `import type` for TypeScript types

## 📚 Documentation Standards

Each major directory should contain:
- **README.md**: Overview and quick start guide
- **Inline Comments**: Complex logic explanation
- **Type Definitions**: Comprehensive TypeScript typing
- **API Documentation**: Endpoint specifications and examples

## 🔄 Build Process

### Development
```bash
# Frontend development server
cd frontend && npm start

# Backend development server  
cd backend && python app.py
```

### Production Build
```bash
# Frontend production build
cd frontend && npm run build

# Backend production deployment
cd backend && gunicorn app:app
```

This structure ensures:
- **Scalability**: Easy to add new features and components
- **Maintainability**: Clear separation of concerns
- **Developer Experience**: Intuitive organization and tooling
- **Performance**: Optimized build processes and asset management