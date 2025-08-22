# Repository Information

This document contains information about the repository structure and components.

## Overview

This repository implements a Domain-Specific Language (DSL) for test data generation. The DSL is designed to simplify and standardize the process of creating test data for software testing purposes.

## Purpose

The Test Data Generation Language (TDGL) aims to:
- Provide a consistent syntax for defining test data requirements
- Enable rapid generation of complex test datasets
- Support various data types and relationships
- Allow for reproducible test data creation
- Reduce the effort required to maintain test data

## Structure

- `/src`: Core implementation of the DSL
- `/examples`: Sample usage patterns and demonstrations
- `/docs`: Documentation for the language and its features
- `/tests`: Test suite for the DSL implementation

## Usage

```
// Example of how to use the DSL
generate TestUser {
  count: 100
  fields {
    id: sequence(1000)
    name: fullName()
    email: email()
    age: integer(18, 65)
    status: oneOf("active", "inactive", "pending")
  }
}
```

## Contributing

Contributions to the Test Data Generation Language are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.
