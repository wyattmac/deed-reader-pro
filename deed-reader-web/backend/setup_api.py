#!/usr/bin/env python3
"""
API Setup Helper for Deed Reader Pro
------------------------------------
This script helps you set up the API configuration properly.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template."""
    env_template = Path("env.template")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✓ .env file already exists")
        return True
    
    if not env_template.exists():
        print("✗ env.template not found!")
        return False
    
    # Copy template to .env
    shutil.copy(env_template, env_file)
    print("✓ Created .env file from template")
    
    # Read and update with placeholder message
    content = env_file.read_text()
    content = content.replace(
        "ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-api-key-here",
        "ANTHROPIC_API_KEY=sk-ant-api03-REPLACE-WITH-YOUR-ACTUAL-KEY"
    )
    env_file.write_text(content)
    
    print("\n⚠️  IMPORTANT: You need to add your Anthropic API key!")
    print("1. Get your API key from: https://console.anthropic.com/settings/keys")
    print("2. Edit .env file and replace 'REPLACE-WITH-YOUR-ACTUAL-KEY' with your actual key")
    print("3. Your .env file is located at:", env_file.absolute())
    
    return True

def install_dependencies():
    """Install required Python packages."""
    print("\n📦 Installing dependencies...")
    
    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("⚠️  WARNING: Not in a virtual environment!")
        print("   It's recommended to use a virtual environment.")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    
    try:
        # Install requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        print("  Try running: pip install -r requirements.txt")
        return False

def test_imports():
    """Test if key imports work."""
    print("\n🧪 Testing imports...")
    
    imports_to_test = [
        ("uvicorn", "FastAPI server"),
        ("fastapi", "FastAPI framework"),
        ("anthropic", "Claude AI client"),
        ("flask", "Flask (for migration)"),
    ]
    
    all_good = True
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            print(f"✓ {description} ({module_name})")
        except ImportError:
            print(f"✗ {description} ({module_name}) - NOT INSTALLED")
            all_good = False
    
    return all_good

def main():
    """Run the setup process."""
    print("=" * 60)
    print("🚀 Deed Reader Pro - API Setup Helper")
    print("=" * 60)
    
    # Step 1: Create .env file
    if not create_env_file():
        print("\n❌ Setup failed: Could not create .env file")
        return 1
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        return 1
    
    # Step 3: Test imports
    if not test_imports():
        print("\n⚠️  Some imports failed. Please install missing packages.")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("1. Add your Anthropic API key to the .env file")
    print("2. Run the migration script: python run_migration.py")
    print("3. Visit http://localhost:8000/api/docs for FastAPI documentation")
    print("4. Run tests: python test_fastapi.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 