#!/bin/bash
# Development environment setup script for Test Data Generation Language on Linux
# This script installs all necessary dependencies and sets up the development environment

set -e  # Exit immediately if a command exits with a non-zero status

echo "Setting up Test Data Generation Language development environment..."

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2)
required_version="3.11.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.11 or higher is required. Found: $python_version"
    echo "Please install Python 3.11+ and try again."
    exit 1
fi

# Install Java (required for ANTLR4)
echo "Installing Java..."
if ! command -v java &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y default-jre
else
    echo "Java is already installed."
fi

# Download ANTLR4
echo "Downloading ANTLR4..."
wget https://www.antlr.org/download/antlr-4.13.2-complete.jar -O /tmp/antlr4.jar

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

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install the package in development mode with all dependencies
echo "Installing package in development mode with all dependencies..."
pip install -e ".[all]"

# Set up pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

echo "Development environment setup completed successfully!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the examples, use:"
echo "  testdatagen validate examples/basic/simple_table.tdg"
echo "  testdatagen generate examples/basic/simple_table.tdg --format json --output ./output"
