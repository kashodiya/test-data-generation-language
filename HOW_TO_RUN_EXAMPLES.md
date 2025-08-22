# How to Run Examples in Test Data Generation Language

This guide provides step-by-step instructions on how to run examples from the Test Data Generation Language repository after cloning it.

## Prerequisites

- Python 3.11 or higher
- Java Runtime Environment (JRE) for ANTLR4 parser generation
- Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/kashodiya/test-data-generation-language.git
cd test-data-generation-language
```

## Step 2: Set Up the Environment

### Automatic Setup with OpenHands

If you're using OpenHands, the setup will be performed automatically when the repository is cloned.

### Manual Setup

If you're not using OpenHands, follow these steps:

1. Install Java (required for ANTLR4):
   ```bash
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y default-jre
   
   # For macOS
   brew install openjdk
   
   # For Windows
   # Download and install JRE from https://www.oracle.com/java/technologies/downloads/
   ```

2. Download ANTLR4:
   ```bash
   wget https://www.antlr.org/download/antlr-4.13.2-complete.jar -O /tmp/antlr4.jar
   ```

3. Generate the parser:
   ```bash
   # Create the generated directory
   mkdir -p src/testdatagen/core/parser/generated
   
   # Generate the lexer
   cd src/testdatagen/core/parser
   java -jar /tmp/antlr4.jar -Dlanguage=Python3 -o generated grammar/TestDataGenLexer.g4
   
   # Generate the parser
   java -jar /tmp/antlr4.jar -Dlanguage=Python3 -visitor -no-listener -lib grammar -o generated grammar/TestDataGen.g4
   
   # Create an __init__.py file in the generated directory
   touch generated/__init__.py
   
   # Go back to the repository root
   cd ../../../..
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Step 3: Run an Example

Once the setup is complete, you can run examples using the `testdatagen` command-line tool:

```bash
# Validate a schema
testdatagen validate examples/basic/simple_table.tdg

# Generate test data
testdatagen generate examples/basic/simple_table.tdg --format json --output ./output
```

### Available Examples

The repository includes several examples:

1. **Basic Example**: A simple schema with basic tables and relationships
   ```bash
   testdatagen generate examples/basic/simple_table.tdg --format json --output ./output
   ```

2. **Advanced Example**: Advanced schema with custom types and complex constraints
   ```bash
   testdatagen generate examples/advanced/custom_types.tdg --format json --output ./output
   ```

## Step 4: Explore the Generated Data

After running the generation command, check the output directory for the generated test data:

```bash
ls -la ./output
```

You should see JSON files containing the generated test data according to your schema definition.

## Troubleshooting

If you encounter any issues:

1. **Parser Generation Errors**: Make sure Java is installed correctly and ANTLR4 jar file is accessible.

2. **Import Errors**: Ensure the package is installed in development mode with `pip install -e .`

3. **Missing Dependencies**: Install any missing dependencies with `pip install -r requirements.txt` (if available) or check the dependencies in `pyproject.toml`.

## Additional Resources

- Check the `README.md` file for more information about the Test Data Generation Language syntax and features.
- Explore the `examples` directory for more example schemas.
- Refer to `IMPLEMENTATION-DESIGN.md` for details about the implementation design.
