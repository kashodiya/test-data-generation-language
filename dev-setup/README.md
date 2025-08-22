

# Development Environment Setup

This directory contains scripts and configuration files to help you set up your development environment for the Test Data Generation Language project.

## Prerequisites

- Python 3.11 or higher
- Java Runtime Environment (JRE) for ANTLR4 parser generation
- Git

## Setup Options

Choose one of the following setup methods based on your operating system and preferences:

### Option 1: Setup with uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver that doesn't require virtual environment activation.

#### For Linux/macOS

```bash
# Make the script executable
chmod +x dev-setup/setup.sh

# Run the setup script
./dev-setup/setup.sh
```

#### For Windows

```powershell
# Run the setup script in PowerShell
.\dev-setup\setup.ps1
```

### Option 2: Docker Setup

If you prefer to use Docker for development:

```bash
# Build and start the Docker container
cd dev-setup
docker-compose up -d

# Enter the container
docker-compose exec testdatagen bash

# Inside the container, you can run commands like:
testdatagen validate examples/basic/simple_table.tdg
```

## What the Setup Scripts Do

The setup scripts perform the following tasks:

1. Check for required dependencies (Python, Java)
2. Download ANTLR4 for parser generation
3. Generate the parser from grammar files
4. Install the package in development mode with all dependencies

The uv setup scripts use uv's built-in isolation features without requiring virtual environment activation.

## Manual Setup

If you prefer to set up your environment manually, follow these steps:

1. Install uv:
   ```bash
   # On Linux/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows (PowerShell)
   iwr -useb https://astral.sh/uv/install.ps1 | iex
   ```

2. Install Java (required for ANTLR4)

3. Download ANTLR4:
   ```bash
   # On Linux/macOS
   curl -o /tmp/antlr4.jar https://www.antlr.org/download/antlr-4.13.2-complete.jar
   
   # On Windows (PowerShell)
   Invoke-WebRequest -Uri "https://www.antlr.org/download/antlr-4.13.2-complete.jar" -OutFile "$env:TEMP\antlr4.jar"
   ```

4. Generate the parser:
   ```bash
   mkdir -p src/testdatagen/core/parser/generated
   cd src/testdatagen/core/parser
   java -jar /tmp/antlr4.jar -Dlanguage=Python3 -o generated grammar/TestDataGenLexer.g4
   java -jar /tmp/antlr4.jar -Dlanguage=Python3 -visitor -no-listener -lib grammar -o generated grammar/TestDataGen.g4
   touch generated/__init__.py
   cd ../../../..
   ```

5. Install the package in development mode with uv:
   ```bash
   uv sync --all-extras
   ```

## Troubleshooting

If you encounter any issues during setup:

1. **Parser Generation Errors**: Make sure Java is installed correctly and ANTLR4 jar file is accessible.

2. **Import Errors**: Ensure the package is installed in development mode with `uv sync --all-extras`

3. **Missing Dependencies**: Run `uv sync --all-extras` to install all dependencies

4. **Package Management Issues**: Run `uv pip list` to check installed packages

5. **Schema Parsing Errors**: If you encounter errors like "mismatched input expecting STRING_LITERAL", there may be a mismatch between the grammar definition and the parser implementation. Try regenerating the parser:
   ```bash
   cd src/testdatagen/core/parser
   java -jar /tmp/antlr4.jar -Dlanguage=Python3 -o generated grammar/TestDataGenLexer.g4
   java -jar /tmp/antlr4.jar -Dlanguage=Python3 -visitor -no-listener -lib grammar -o generated grammar/TestDataGen.g4
   touch generated/__init__.py
   ```

