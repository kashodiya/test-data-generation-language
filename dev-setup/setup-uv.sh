#!/bin/bash
# Development environment setup script for Test Data Generation Language using uv
# This script installs all necessary dependencies and sets up the development environment

set -e  # Exit immediately if a command exits with a non-zero status

echo "Setting up Test Data Generation Language development environment with uv..."

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2)
required_version="3.11.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.11 or higher is required. Found: $python_version"
    echo "Please install Python 3.11+ and try again."
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for the current session
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Install Java (required for ANTLR4)
echo "Installing Java..."
if ! command -v java &> /dev/null; then
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y default-jre
    elif command -v brew &> /dev/null; then
        brew install openjdk
    else
        echo "Please install Java manually and run this script again."
        exit 1
    fi
else
    echo "Java is already installed."
fi

# Download ANTLR4
echo "Downloading ANTLR4..."
if [ ! -f "/tmp/antlr4.jar" ]; then
    curl -o /tmp/antlr4.jar https://www.antlr.org/download/antlr-4.13.2-complete.jar
fi

# Create the generated directory
echo "Creating parser directories..."
mkdir -p src/testdatagen/core/parser/generated

# Generate the parser
echo "Generating parser..."
cd src/testdatagen/core/parser

# First generate the lexer
java -jar /tmp/antlr4.jar -Dlanguage=Python3 -o generated grammar/TestDataGenLexer.g4

# Then generate the parser with the lexer
java -jar /tmp/antlr4.jar -Dlanguage=Python3 -visitor -no-listener -lib grammar -o generated grammar/TestDataGen.g4

# Create an __init__.py file in the generated directory
touch generated/__init__.py

# Go back to the repository root
cd ../../../..

# Install the package in development mode with all dependencies using uv
echo "Installing package in development mode with all dependencies using uv..."
uv pip install -e ".[all]"

echo "Development environment setup completed successfully!"
echo ""
echo "You can now run the examples directly using:"
echo "  testdatagen validate examples/basic/simple_table.tdg"
echo "  testdatagen generate examples/basic/simple_table.tdg --format json --output ./output"
echo ""
echo "No virtual environment activation is needed with uv!"
