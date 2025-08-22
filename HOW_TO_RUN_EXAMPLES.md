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

### Development Environment Setup

For setting up your development environment, please refer to the detailed instructions in the `dev-setup/README.md` file. The dev-setup directory contains scripts for different operating systems and a Docker option:

1. **Native Setup with uv (Recommended)**:
   - For Linux/macOS:
     ```bash
     ./dev-setup/setup-uv.sh
     ```
   - For Windows:
     ```powershell
     .\dev-setup\setup-uv.ps1
     ```

2. **Traditional Setup**:
   - For Linux: `./dev-setup/setup-linux.sh`
   - For macOS: `./dev-setup/setup-macos.sh`
   - For Windows: `.\dev-setup\setup-windows.ps1`

3. **Docker Setup**:
   ```bash
   cd dev-setup
   docker-compose up -d
   docker-compose exec testdatagen bash
   ```

These setup scripts will:
- Check for required dependencies (Python, Java)
- Download ANTLR4 for parser generation
- Generate the parser from grammar files
- Install the package in development mode with all dependencies
- With uv setup, no virtual environment activation is needed

For more details or troubleshooting, see `dev-setup/README.md`.

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

If you encounter any issues during setup or execution:

1. **Setup Issues**: Refer to the troubleshooting section in `dev-setup/README.md` for detailed guidance on resolving common setup problems.

2. **Parser Generation Errors**: Make sure Java is installed correctly and ANTLR4 jar file is accessible.

3. **Import Errors**: 
   - With uv: Ensure the package is installed in development mode with `uv pip install -e ".[all]"`
   - With pip: Ensure the package is installed in development mode with `pip install -e ".[all]"` as described in the setup scripts.

4. **Missing Dependencies**: 
   - With uv: Run `uv pip install -e ".[all]"` to install all dependencies
   - With pip: Check the dependencies in `pyproject.toml` and make sure they're installed correctly.

5. **Package Management Issues**: 
   - If using uv: Run `uv pip list` to check installed packages
   - If using traditional setup: Ensure your virtual environment is activated with `source .venv/bin/activate` (Linux/macOS) or `.\.venv\Scripts\activate` (Windows)

6. **Schema Parsing Errors**: If you encounter errors like "mismatched input expecting STRING_LITERAL", there may be a mismatch between the grammar definition and the parser implementation. Try using the dev-setup scripts to regenerate the parser correctly.

## Additional Resources

- Check the `README.md` file for more information about the Test Data Generation Language syntax and features.
- Explore the `examples` directory for more example schemas.
- Refer to `IMPLEMENTATION-DESIGN.md` for details about the implementation design.
- Use the setup scripts and instructions in the `dev-setup` directory for configuring your development environment.
