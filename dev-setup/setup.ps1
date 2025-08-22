
# Development environment setup script for Test Data Generation Language using uv
# This script installs all necessary dependencies and sets up the development environment

Write-Host "Setting up Test Data Generation Language development environment with uv..."

# Check Python version
$pythonVersion = (python --version).Split(" ")[1]
$requiredVersion = "3.11.0"

if ([version]$pythonVersion -lt [version]$requiredVersion) {
    Write-Host "Error: Python 3.11 or higher is required. Found: $pythonVersion"
    Write-Host "Please install Python 3.11+ and try again."
    exit 1
}

# Check if uv is installed
try {
    $uvVersion = uv --version
    Write-Host "uv is already installed: $uvVersion"
} catch {
    Write-Host "Installing uv package manager..."
    iwr -useb https://astral.sh/uv/install.ps1 | iex
}

# Check if Java is installed
try {
    $javaVersion = (java -version 2>&1 | Out-String)
    Write-Host "Java is already installed."
} catch {
    Write-Host "Java is required for ANTLR4. Please install Java and make sure it's in your PATH."
    Write-Host "You can download it from: https://adoptium.net/"
    exit 1
}

# Download ANTLR4
Write-Host "Downloading ANTLR4..."
$antlrJarPath = "$env:TEMP\antlr4.jar"
if (-not (Test-Path $antlrJarPath)) {
    Invoke-WebRequest -Uri "https://www.antlr.org/download/antlr-4.13.2-complete.jar" -OutFile $antlrJarPath
}

# Create the generated directory
Write-Host "Creating parser directories..."
New-Item -ItemType Directory -Force -Path "src\testdatagen\core\parser\generated" | Out-Null

# Generate the parser
Write-Host "Generating parser..."
Set-Location -Path "src\testdatagen\core\parser"

# First generate the lexer
java -jar $antlrJarPath -Dlanguage=Python3 -o generated grammar\TestDataGenLexer.g4

# Then generate the parser with the lexer
java -jar $antlrJarPath -Dlanguage=Python3 -visitor -no-listener -lib grammar -o generated grammar\TestDataGen.g4

# Create an __init__.py file in the generated directory
New-Item -ItemType File -Force -Path "generated\__init__.py" | Out-Null

# Move the generated files from the grammar subdirectory to the generated directory
Write-Host "Moving generated files to the correct location..."
Copy-Item -Path "generated\grammar\*.py" -Destination "generated\" -Force
New-Item -ItemType File -Force -Path "generated\__init__.py" | Out-Null

# Go back to the repository root
Set-Location -Path "..\..\..\..\"

# Install the package in development mode with all dependencies using uv
Write-Host "Installing package in development mode with all dependencies using uv..."
uv sync --all-extras

Write-Host "Development environment setup completed successfully!"
Write-Host ""
Write-Host "You can now run the examples directly using:"
Write-Host "  uv run testdatagen validate examples\basic\simple_table.tdg"
Write-Host "  uv run testdatagen generate examples\basic\simple_table.tdg --format json --output .\output"
Write-Host ""
Write-Host "No virtual environment activation is needed with uv!"
