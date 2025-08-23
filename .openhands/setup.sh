#!/bin/bash
echo "Setting up dev env..."
echo "Current directory is: $(pwd)"
chmod +x dev-setup/setup.sh
./dev-setup/setup.sh
echo "Dev env setup done!"


# # setup.sh for Test Data Generation Language repository
# # This script will be executed automatically by OpenHands when the repository is cloned

# set -e  # Exit immediately if a command exits with a non-zero status

# echo "Setting up Test Data Generation Language repository..."

# # Install Java (required for ANTLR4)
# echo "Installing Java..."
# apt-get update
# apt-get install -y default-jre

# # Download ANTLR4
# echo "Downloading ANTLR4..."
# wget https://www.antlr.org/download/antlr-4.13.2-complete.jar -O /tmp/antlr4.jar

# # Create the generated directory
# echo "Creating parser directories..."
# mkdir -p src/testdatagen/core/parser/generated

# # Generate the parser
# echo "Generating parser..."
# cd src/testdatagen/core/parser

# # First generate the lexer
# java -jar /tmp/antlr4.jar -Dlanguage=Python3 -o generated grammar/TestDataGenLexer.g4

# # Then generate the parser with the lexer
# java -jar /tmp/antlr4.jar -Dlanguage=Python3 -visitor -no-listener -lib grammar -o generated grammar/TestDataGen.g4

# # Create an __init__.py file in the generated directory
# touch generated/__init__.py

# # Go back to the repository root
# cd ../../../..

# # Install the package in development mode
# echo "Installing package in development mode..."
# pip install -e .

# echo "Setup completed successfully!"
