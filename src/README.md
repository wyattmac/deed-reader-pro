# Source Code Directory

This directory contains the main application source code.

Since `deed-reader-web` couldn't be moved due to file permissions, it remains in the root directory but is organized as follows:

## Current Structure
```
../deed-reader-web/          # Main application (in root due to permissions)
├── frontend/                # React TypeScript frontend
├── backend/                 # Flask Python backend
└── README.md               # Application documentation
```

## Recommended Structure
When setting up a new environment, organize as:
```
src/
├── frontend/               # React application
├── backend/                # Flask API
└── shared/                # Shared utilities
```

For now, all source code operations should reference `../deed-reader-web/` from this directory.