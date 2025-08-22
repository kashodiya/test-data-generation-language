
#!/usr/bin/env python3
"""
Check if the development environment is properly set up for Test Data Generation Language.
This script verifies that all required dependencies are installed and the parser is generated.
"""

import importlib
import os
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.11 or higher."""
    required_version = (3, 11)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"❌ Python 3.11+ is required. Found: {sys.version.split()[0]}")
        return False
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")
        return True


def check_java():
    """Check if Java is installed."""
    try:
        result = subprocess.run(
            ["java", "-version"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        if result.returncode == 0:
            java_version = result.stderr.split("\n")[0]
            print(f"✅ Java is installed: {java_version}")
            return True
        else:
            print("❌ Java is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ Java is not installed or not in PATH")
        return False


def check_parser_generated():
    """Check if the parser has been generated."""
    parser_dir = Path("src/testdatagen/core/parser/generated")
    
    if not parser_dir.exists():
        print("❌ Parser directory does not exist")
        return False
    
    lexer_file = parser_dir / "TestDataGenLexer.py"
    parser_file = parser_dir / "TestDataGen.py"
    
    if not lexer_file.exists() or not parser_file.exists():
        print("❌ Parser files are missing")
        return False
    
    print("✅ Parser files are present")
    return True


def check_package_installed():
    """Check if the package is installed in development mode."""
    try:
        importlib.import_module("testdatagen")
        print("✅ Package is installed")
        return True
    except ImportError:
        print("❌ Package is not installed")
        return False


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        "antlr4-python3-runtime",
        "pydantic",
        "jinja2",
        "pandas",
        "numpy",
        "sqlalchemy",
        "click",
        "rich",
        "faker",
        "fastapi",
        "pygls",
        "pyyaml",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.split("[")[0])
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing dependencies: {', '.join(missing_packages)}")
        return False
    else:
        print("✅ All core dependencies are installed")
        return True


def check_pre_commit():
    """Check if pre-commit hooks are installed (optional)."""
    pre_commit_file = Path(".git/hooks/pre-commit")
    
    if pre_commit_file.exists():
        print("✅ Pre-commit hooks are installed")
        return True
    else:
        print("ℹ️ Pre-commit hooks are not installed (optional)")
        return True  # Return True since this is now optional


def main():
    """Run all checks and report results."""
    print("Checking development environment for Test Data Generation Language...\n")
    
    checks = [
        check_python_version(),
        check_java(),
        check_parser_generated(),
        check_package_installed(),
        check_dependencies(),
        check_pre_commit()
    ]
    
    print("\nSummary:")
    if all(checks):
        print("✅ All checks passed! Your development environment is properly set up.")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        
        # Provide suggestions
        print("\nSuggestions:")
        print("1. Run the appropriate setup script for your OS from the dev-setup directory")
        print("2. Make sure Java is installed and in your PATH")
        print("3. Generate the parser manually if needed")
        print("4. Install the package in development mode with: pip install -e \".[all]\"")
        # Pre-commit hooks suggestion removed as per user request


if __name__ == "__main__":
    main()
