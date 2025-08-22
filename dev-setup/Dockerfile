
# Development Dockerfile for Test Data Generation Language
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre \
    wget \
    git \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Download ANTLR4
RUN wget https://www.antlr.org/download/antlr-4.13.2-complete.jar -O /tmp/antlr4.jar

# Copy the project files
COPY . /app/

# Create the generated directory
RUN mkdir -p src/testdatagen/core/parser/generated

# Generate the parser
WORKDIR /app/src/testdatagen/core/parser
RUN java -jar /tmp/antlr4.jar -Dlanguage=Python3 -o generated grammar/TestDataGenLexer.g4 && \
    java -jar /tmp/antlr4.jar -Dlanguage=Python3 -visitor -no-listener -lib grammar -o generated grammar/TestDataGen.g4 && \
    touch generated/__init__.py

# Return to the app directory
WORKDIR /app

# Install the package in development mode with all dependencies
RUN pip install --no-cache-dir -e ".[all]"

# Set up pre-commit hooks
RUN pre-commit install

# Default command
CMD ["bash"]
