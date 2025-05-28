# 🏠 Deed Reader Pro - Organized Structure

Welcome to the newly organized Deed Reader Pro project! Files have been reorganized into logical directories for better maintainability.

## 📁 Directory Structure

```
dEED READ/
├── 📚 docs/                    # All documentation
│   ├── README.md               # Main project documentation  
│   ├── CONTRIBUTING.md         # Development guidelines
│   ├── PROJECT_STRUCTURE.md    # Detailed folder structure
│   ├── ENHANCEMENT_PLAN.md     # Future improvements
│   └── QUICK_START.txt         # Quick reference
│
├── 🚀 scripts/                 # Automation scripts
│   ├── RUN_APP.bat             # Main launcher
│   ├── TROUBLESHOOT.bat        # Diagnostic tool
│   ├── CHECK_STATUS.bat        # Status checker  
│   ├── LINT_ALL.bat            # Linting tools
│   └── *.bat                   # Other utility scripts
│
├── 🗂️ deed-reader-web/         # Source code (main application)
│   ├── frontend/               # React TypeScript app
│   ├── backend/                # Flask Python API
│   └── README.md               # Technical documentation
│
├── ⚙️ config/                  # Configuration files
│   ├── CLAUDE.md               # Claude Code instructions
│   ├── .pre-commit-config.yaml # Pre-commit hooks
│   └── CLAUDE.local.md         # Local overrides
│
├── 📋 samples/                 # Sample files & test data
│   ├── sample_simple_deed.txt  # Test deed document
│   └── tint_rd.pdf             # Sample PDF
│
├── 🏗️ build/                   # Build artifacts (when generated)
└── 🗂️ src/                     # Additional source organization
```

## 🚀 Quick Start

1. **Set up GitHub (First time only):**
   ```bash
   scripts/GIT_SETUP.bat   # Configure git and connect to GitHub
   ```

2. **Launch the application:**
   ```bash
   scripts/RUN_APP.bat     # Start both frontend and backend
   ```

3. **Make commits:**
   ```bash
   scripts/GIT_COMMIT.bat  # Easy commit and push workflow
   ```

4. **Read documentation:**
   ```bash
   docs/README.md          # Start here
   docs/GITHUB_SETUP.md    # GitHub connection guide
   ```

5. **Troubleshoot issues:**
   ```bash
   scripts/TROUBLESHOOT.bat
   ```

## 📝 Important Notes

- **Scripts automatically adjust paths** - no manual changes needed
- **Documentation moved to `docs/`** - check there for guides
- **Main source code** remains in `deed-reader-web/` (due to file permissions)
- **All batch scripts** moved to `scripts/` directory

## 🔧 Configuration

Configuration files are now in the `config/` directory:
- `config/CLAUDE.md` - Instructions for Claude Code
- `config/.pre-commit-config.yaml` - Git hooks setup

## 📚 Documentation

All documentation is now centralized in the `docs/` directory:
- **Main README** - Project overview and setup
- **CONTRIBUTING** - Development workflow and standards  
- **PROJECT_STRUCTURE** - Detailed file organization
- **ENHANCEMENT_PLAN** - Planned improvements

---

**🎯 Everything you need is organized and ready to go!**  
Start with `scripts/RUN_APP.bat` to launch the application.