#!/usr/bin/env python3
"""
Linting script for the Deed Reader backend
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print results"""
    print(f"\n{'='*60}")
    print(f"Running {description}...")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode

def main():
    """Run all linting tools"""
    exit_code = 0
    
    # Get the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    
    # Run flake8
    if run_command("flake8 .", "Flake8 (style guide)") != 0:
        exit_code = 1
    
    # Run black in check mode
    if run_command("black --check .", "Black (formatting check)") != 0:
        exit_code = 1
        print("\nTo fix formatting issues, run: black .")
    
    # Run isort in check mode
    if run_command("isort --check-only .", "isort (import sorting)") != 0:
        exit_code = 1
        print("\nTo fix import sorting, run: isort .")
    
    # Run mypy (optional, may need configuration)
    # Uncomment when ready to use type checking
    # if run_command("mypy .", "mypy (type checking)") != 0:
    #     exit_code = 1
    
    print(f"\n{'='*60}")
    if exit_code == 0:
        print("✅ All linting checks passed!")
    else:
        print("❌ Some linting checks failed. Please fix the issues above.")
    print(f"{'='*60}")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())