# Test Data Generation Language (TDGL)

A domain-specific language designed to simplify and standardize the process of generating test data for software testing.

## Overview

TDGL provides a declarative syntax for defining test data requirements, enabling developers and QA engineers to quickly generate complex, realistic test datasets with minimal effort.

## Features

- **Schema Definition**: Define database schemas with tables, fields, and relationships
- **Rich Type System**: Support for primitive types, composite types, and custom types
- **Constraints**: Define value constraints, business rules, and relationships
- **Data Generation**: Generate realistic test data using various strategies
- **Export Formats**: Export generated data to JSON, CSV, PostgreSQL SQL scripts, and other formats
- **CLI Interface**: Command-line interface for validating schemas and generating data

## Installation

### For Users

```bash
pip install testdatagen
```

### For Developers

We provide setup scripts to help you set up your development environment:

```bash
# For Linux
./dev-setup/setup-linux.sh

# For macOS
./dev-setup/setup-macos.sh

# For Windows (PowerShell)
.\dev-setup\setup-windows.ps1
```

For more detailed instructions, see the [Development Setup Guide](./dev-setup/README.md).


## Quick Start

1. Define your schema in a `.tdg` file:

```
schema "TestDatabase" {
    table User {
        field id: integer with primary key;
        field username: string with not null;
        field email: string with not null;
        field created_at: timestamp with not null;
        
        constraint unique(username);
        constraint unique(email);
        
        generate {
            count = 100,
            strategy = "faker"
        };
    }
}
```

> **Note**: The schema name can be either quoted (`schema "TestDatabase" {`) or unquoted (`schema TestDatabase {`). The parser has been modified to handle both formats.

2. Validate your schema:

```bash
testdatagen validate schema.tdg
```

3. Generate test data:

```bash
# Generate JSON data
testdatagen generate schema.tdg --count 100 --format json --output ./output

# Generate CSV data
testdatagen generate schema.tdg --count 100 --format csv --output ./output

# Generate PostgreSQL SQL scripts
testdatagen generate schema.tdg --format postgresql --output ./output --pg-schema myschema --pg-create-schema
```

## Schema Name Format

The parser supports both quoted and unquoted schema names:

```
# Quoted schema name (recommended)
schema "TestDatabase" {
    // ...
}

# Unquoted schema name (also supported)
schema TestDatabase {
    // ...
}
```

We've implemented a wrapper script that automatically handles both formats. If you encounter any issues with schema name format, you can use one of the following solutions:

1. Use the wrapper script:
   ```bash
   python validate_wrapper.py examples/basic/simple.tdg
   ```

2. Use the modified parser (installed as the default `testdatagen` command)

3. Manually add quotes around your schema name in your `.tdg` file

## Syntax

### Schema Definition

```
schema SchemaName {
    // Tables, types, and other definitions
}
```

### Table Definition

```
table TableName {
    // Fields and constraints
    
    generate {
        // Generation options
    };
}
```

### Field Definition

```
field FieldName: DataType with Constraint1, Constraint2;
```

### Constraints

```
constraint primary key(field1, field2);
constraint foreign key(field1) references OtherTable(other_field);
constraint unique(field1, field2);
constraint check(expression);
```

### Custom Types

```
type EmailType = string with pattern("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$");
type Rating = integer with range(1, 5);
type Status = enum("pending", "processing", "shipped", "delivered", "cancelled");
```

## Examples

See the `examples` directory for more examples:

- `examples/basic/simple_table.tdg`: A simple schema with basic tables and relationships
- `examples/advanced/custom_types.tdg`: Advanced schema with custom types and complex constraints
- `examples/postgresql/postgres_example.tdg`: Example schema for PostgreSQL export with database-specific features

### PostgreSQL Export

The PostgreSQL export feature allows you to generate SQL scripts that can be directly executed in PostgreSQL databases:

```bash
# Basic PostgreSQL export
testdatagen generate schema.tdg --format postgresql --output ./output

# With PostgreSQL-specific options
testdatagen generate schema.tdg --format postgresql --output ./output \
  --pg-schema myschema --pg-create-schema --pg-single-file
```

PostgreSQL-specific options:
- `--pg-schema`: The PostgreSQL schema name (default: "public")
- `--pg-create-schema`: Include schema creation statements
- `--pg-single-file`: Export all tables to a single SQL file

For more details, see the [PostgreSQL Export documentation](./examples/postgresql/README.md).

