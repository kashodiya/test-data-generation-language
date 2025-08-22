
# Development environment setup script for Test Data Generation Language on Windows
# This script installs all necessary dependencies and sets up the development environment

# Function to check if a command exists
function Test-CommandExists {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $command) { return $true }
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
}

Write-Host "Setting up Test Data Generation Language development environment..." -ForegroundColor Green

# Check Python version
$pythonVersion = (python --version).Split(" ")[1]
$requiredVersion = "3.11.0"

if ([version]$pythonVersion -lt [version]$requiredVersion) {
    Write-Host "Error: Python 3.11 or higher is required. Found: $pythonVersion" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://www.python.org/downloads/ and try again." -ForegroundColor Red
    exit 1
}

# Check if Java is installed
if (-not (Test-CommandExists java)) {
    Write-Host "Java is not installed. Please install Java from https://www.oracle.com/java/technologies/downloads/" -ForegroundColor Red
    Write-Host "After installing Java, please run this script again." -ForegroundColor Red
    exit 1
} else {
    Write-Host "Java is already installed." -ForegroundColor Green
}

# Download ANTLR4
Write-Host "Downloading ANTLR4..." -ForegroundColor Green
$antlrUrl = "https://www.antlr.org/download/antlr-4.13.2-complete.jar"
$antlrPath = "$env:TEMP\antlr4.jar"
Invoke-WebRequest -Uri $antlrUrl -OutFile $antlrPath

# Create the generated directory
Write-Host "Creating parser directories..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "src\testdatagen\core\parser\generated" | Out-Null

# Generate the parser
Write-Host "Generating parser..." -ForegroundColor Green
Push-Location "src\testdatagen\core\parser"

# First generate the lexer
java -jar $antlrPath -Dlanguage=Python3 -o generated grammar/TestDataGenLexer.g4

# Then generate the parser with the lexer
java -jar $antlrPath -Dlanguage=Python3 -visitor -no-listener -lib grammar -o generated grammar/TestDataGen.g4

# Create an __init__.py file in the generated directory
New-Item -ItemType File -Force -Path "generated\__init__.py" | Out-Null

# Go back to the repository root
Pop-Location

# Create a virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Green
python -m venv .venv

# Activate the virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

# Install the package in development mode with all dependencies
Write-Host "Installing package in development mode with all dependencies..." -ForegroundColor Green
pip install -e ".[all]"

# Set up pre-commit hooks
Write-Host "Setting up pre-commit hooks..." -ForegroundColor Green
pre-commit install

Write-Host "Development environment setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the virtual environment, run:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the examples, use:" -ForegroundColor Cyan
Write-Host "  testdatagen validate examples\basic\simple_table.tdg" -ForegroundColor Cyan
Write-Host "  testdatagen generate examples\basic\simple_table.tdg --format json --output .\output" -ForegroundColor Cyan

