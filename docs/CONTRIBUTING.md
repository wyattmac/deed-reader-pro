# Contributing to Deed Reader Pro

Thank you for considering contributing to Deed Reader Pro! This document outlines our development workflow and coding standards.

## 🌿 Branch Naming Conventions

We follow a structured branch naming convention to keep our repository organized:

### Branch Types

```bash
# Feature branches - New functionality
feature/authentication-system
feature/pdf-ocr-enhancement
feature/coordinate-plotting
feature/export-to-csv

# Bug fixes - Fixing existing issues
bugfix/file-upload-validation
bugfix/claude-api-timeout
bugfix/plotting-accuracy

# Hotfixes - Critical production fixes
hotfix/security-vulnerability
hotfix/api-key-leak

# Chores - Maintenance, dependencies, tooling
chore/update-dependencies
chore/improve-testing
chore/setup-linting

# Documentation - Docs, README updates
docs/api-documentation
docs/setup-guide-improvements
docs/contributing-guidelines
```

### Branch Naming Rules

1. **Use lowercase letters** and hyphens (kebab-case)
2. **Be descriptive** but concise
3. **Use present tense** (e.g., `add-user-auth` not `added-user-auth`)
4. **Reference issue numbers** when applicable: `feature/123-coordinate-parsing`

### Examples

```bash
# ✅ Good branch names
feature/claude-vision-integration
bugfix/pdf-text-extraction
chore/update-react-dependencies
docs/installation-improvements

# ❌ Avoid these patterns
Feature/ClaudeVision          # Wrong case
feature_claude_vision         # Use hyphens, not underscores
claude-vision                 # Missing type prefix
feature/fix-bug               # Contradictory type/action
```

## 🔄 Development Workflow

1. **Create a feature branch** from `main`
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards
3. **Test thoroughly** using provided test scripts
4. **Run linting** before committing
   ```bash
   LINT_ALL.bat  # Windows
   # OR
   npm run lint && python lint.py
   ```

5. **Commit with descriptive messages**
   ```bash
   git commit -m "Add Claude Vision API integration for scanned PDFs"
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 🏗️ Folder Structure Standards

### Frontend Structure
```
src/
├── components/          # Reusable UI components
│   ├── UI/             # Generic UI elements (Button, Modal, etc.)
│   ├── Forms/          # Form-specific components
│   ├── Layout/         # Layout components (Header, Sidebar)
│   └── Plot/           # Plotting-specific components
├── pages/              # Route-level components
├── hooks/              # Custom React hooks
├── services/           # API calls and external services
├── utils/              # Pure utility functions
├── types/              # TypeScript type definitions
├── constants/          # Application constants
└── styles/             # Global styles (if not using Tailwind)
```

### Backend Structure
```
backend/
├── app.py              # Main Flask application
├── routes/             # API route handlers
├── services/           # Business logic layer
├── core/               # Core parsing algorithms
├── tests/              # Test files
└── utils/              # Utility functions
```

## 📝 Coding Standards

### Frontend (TypeScript/React)
- Use **functional components** with hooks
- Follow **React naming conventions** (PascalCase for components)
- Use **TypeScript** for all new code
- Implement **error boundaries** for robust error handling
- Use **Tailwind CSS** for styling

### Backend (Python)
- Follow **PEP 8** style guidelines
- Use **type hints** where applicable
- Implement proper **error handling**
- Write **docstrings** for functions and classes
- Use **environment variables** for configuration

### General
- Write **clear, descriptive commit messages**
- Add **comments** for complex logic
- Follow **DRY principles** (Don't Repeat Yourself)
- Ensure **responsive design** for all UI components

## 🧪 Testing Requirements

Before submitting a pull request:

1. **Frontend**: Ensure components render without errors
2. **Backend**: Run all test scripts in `/backend/`
3. **Integration**: Test the complete workflow end-to-end
4. **Linting**: All code must pass linting checks

## 📋 Pull Request Checklist

- [ ] Branch follows naming convention
- [ ] Code follows project standards
- [ ] All tests pass
- [ ] Linting passes (`LINT_ALL.bat`)
- [ ] Documentation updated if needed
- [ ] Environment variables documented in `.env.example`
- [ ] No sensitive data committed

## 🐛 Issue Reporting

When reporting issues:

1. **Use descriptive titles**
2. **Provide reproduction steps**
3. **Include error messages/screenshots**
4. **Specify environment** (OS, browser, Python version)

## 🚀 Release Process

1. **Feature freeze** on release candidate branch
2. **Comprehensive testing** across all supported environments
3. **Update version numbers** in relevant files
4. **Tag release** with semantic versioning (v1.2.3)
5. **Deploy to production** using established procedures

---

## Questions?

Feel free to open an issue or start a discussion if you have questions about contributing!