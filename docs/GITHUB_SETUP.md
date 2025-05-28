# 🐙 GitHub Setup Guide

This guide will help you connect your Deed Reader Pro project to GitHub for version control and collaboration.

## 🔧 Step 1: Configure Git User (Required)

First, set up your git identity:

```bash
# Replace with your actual name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Optional: Set default branch name
git config --global init.defaultBranch main
```

## 🔑 Step 2: Set Up Authentication

Choose one of these methods:

### Option A: HTTPS with Personal Access Token (Recommended)
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`, `write:packages`
4. Copy the token (save it securely!)

### Option B: SSH Key Setup
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub

# Add the key to GitHub: Settings > SSH and GPG keys > New SSH key
```

## 🏗️ Step 3: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon → "New repository"
3. Repository settings:
   - **Name**: `deed-reader-pro` (or your preferred name)
   - **Description**: "AI-powered deed document analysis application"
   - **Visibility**: Private (recommended) or Public
   - **DO NOT** initialize with README, .gitignore, or license (we have these)

## 🔗 Step 4: Connect Local Repository to GitHub

After creating the GitHub repository, connect it:

```bash
# Replace YOUR_USERNAME and REPOSITORY_NAME with actual values
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git

# Or with SSH (if you set up SSH keys):
# git remote add origin git@github.com:YOUR_USERNAME/REPOSITORY_NAME.git

# Verify connection
git remote -v
```

## 📤 Step 5: Make Initial Commit and Push

```bash
# Stage all files
git add .

# Make initial commit
git commit -m "Initial commit: Deed Reader Pro setup

🚀 Features:
- React TypeScript frontend
- Flask Python backend  
- Claude AI integration
- Professional project structure
- Linting and pre-commit hooks
- Comprehensive documentation

🤖 Generated with Claude Code
https://claude.ai/code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub
git push -u origin main
```

## 🎯 Step 6: Verify Setup

Check that everything worked:

1. Visit your GitHub repository URL
2. You should see all your project files
3. Try making a small change and pushing:

```bash
# Make a small change
echo "# Last updated: $(date)" >> README.md

# Commit and push
git add README.md
git commit -m "docs: update README with timestamp"
git push
```

## 🔧 Automated Scripts

I've created these helper scripts for you:

### `scripts/GIT_SETUP.bat` (Run this first)
```bash
# This will guide you through the setup process
scripts/GIT_SETUP.bat
```

### `scripts/GIT_COMMIT.bat` (Use for regular commits)
```bash
# This will help you make commits easily
scripts/GIT_COMMIT.bat
```

## 🛡️ Security Best Practices

### ✅ Do:
- Use Personal Access Tokens for HTTPS
- Keep your tokens secure and private
- Use meaningful commit messages
- Review changes before pushing

### ❌ Don't:
- Commit API keys or passwords (use .env files)
- Push large binary files
- Force push to main branch
- Share your access tokens

## 🔄 Common Git Commands

```bash
# Check status
git status

# Stage changes
git add .
git add specific-file.txt

# Commit changes
git commit -m "your commit message"

# Push changes
git push

# Pull latest changes
git pull

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main
git checkout feature-branch

# Merge branch
git checkout main
git merge feature/new-feature
```

## 🆘 Troubleshooting

### Authentication Issues
```bash
# If HTTPS authentication fails, update credentials:
git config --global credential.helper manager

# Test connection:
git ls-remote origin
```

### Push Rejected
```bash
# If push is rejected, pull first:
git pull origin main
git push origin main
```

### Large Files
```bash
# If files are too large, use Git LFS:
git lfs install
git lfs track "*.pdf"
git add .gitattributes
```

## 📚 Next Steps

After connecting to GitHub:

1. **Set up branch protection rules** in GitHub repository settings
2. **Enable GitHub Actions** for CI/CD workflows  
3. **Add collaborators** if working with a team
4. **Create issues and milestones** for project management
5. **Set up GitHub Pages** for documentation hosting

---

**🎉 Once connected, you'll have professional version control for your Deed Reader Pro project!**