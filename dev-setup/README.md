

# Development Environment Setup

This directory contains scripts and configuration files to help you set up your development environment for the Test Data Generation Language project.

## Prerequisites

- Python 3.11 or higher
- Java Runtime Environment (JRE) for ANTLR4 parser generation
- Git

## Setup Options

Choose one of the following setup methods based on your operating system and preferences:

### Option 1: Native Setup

#### For Linux

```bash
# Make the script executable
chmod +x dev-setup/setup-linux.sh

# Run the setup script
./dev-setup/setup-linux.sh
```

#### For macOS

```bash
# Make the script executable
chmod +x dev-setup/setup-macos.sh

# Run the setup script
./dev-setup/setup-macos.sh
```

#### For Windows

```powershell
# Run the setup script in PowerShell
.\dev-setup\setup-windows.ps1
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
4. Create a virtual environment
5. Install the package in development mode with all dependencies

## Manual Setup

If you prefer to set up your environment manually, follow these steps:

1. Install Java (required for ANTLR4)
2. Download ANTLR4:
   ```bash
   wget https://www.antlr.org/download/antlr-4.13.2-complete.jar -O /tmp/antlr4.jar
   ```
3. Generate the parser:
   ```bash
   mkdir -p src/testdatagen/core/parser/generated
   cd src/testdatagen/core/parser
   java -jar /tmp/antlr4.jar -Dlanguage=Python3 -o generated grammar/TestDataGenLexer.g4
   java -jar /tmp/antlr4.jar -Dlanguage=Python3 -visitor -no-listener -lib grammar -o generated grammar/TestDataGen.g4
   touch generated/__init__.py
   cd ../../../..
   ```
4. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
   ```
5. Install the package in development mode:
   ```bash
   pip install -e ".[all]"
   ```

## Troubleshooting

If you encounter any issues during setup:

1. **Parser Generation Errors**: Make sure Java is installed correctly and ANTLR4 jar file is accessible.

2. **Import Errors**: Ensure the package is installed in development mode with `pip install -e .`

3. **Missing Dependencies**: Check the dependencies in `pyproject.toml`.

4. **Virtual Environment Issues**: If you have problems with the virtual environment, try creating it manually:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
   pip install -e ".[all]"
   ```

