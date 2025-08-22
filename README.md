# Test Data Generation Language (TDGL)

A domain-specific language designed to simplify and standardize the process of generating test data for software testing.

## Overview

TDGL provides a declarative syntax for defining test data requirements, enabling developers and QA engineers to quickly generate complex, realistic test datasets with minimal effort.

## Features

- **Simple, Declarative Syntax**: Define your data needs in a readable, maintainable format
- **Rich Data Types**: Support for primitive types, complex objects, and relationships
- **Data Constraints**: Specify validation rules and relationships between data elements
- **Extensible**: Create custom data generators for domain-specific needs
- **Output Formats**: Generate data in various formats (JSON, CSV, SQL, etc.)

## Quick Start

```
// Define a simple user data model
generate User {
  count: 1000
  fields {
    id: sequence(1)
    username: username()
    email: email(domain: "example.com")
    created_at: datetime(from: "2023-01-01", to: "now")
    is_active: boolean(trueWeight: 0.8)
  }
}

// Generate related data
generate Order {
  count: 5000
  fields {
    id: sequence(1)
    user_id: reference(User.id)
    amount: decimal(10.00, 1000.00)
    status: oneOf("pending", "processing", "shipped", "delivered", "cancelled")
    items: integer(1, 10)
  }
}
```

## Getting Started

The implementation details and installation process will be determined as the project develops. Stay tuned for updates on how to install and use the language.

