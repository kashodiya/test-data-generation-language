# PostgreSQL Export Feature

This directory contains examples demonstrating the PostgreSQL export feature of the Test Data Generation Language.

## Overview

The PostgreSQL export feature allows you to generate SQL scripts that can be directly executed in PostgreSQL to:

1. Create database schemas
2. Create tables with appropriate data types
3. Define constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK)
4. Insert generated test data

## Usage

To generate PostgreSQL SQL scripts from a schema file:

```bash
# Basic usage
uv run testdatagen generate postgres_example.tdg --format postgresql --output ./output

# With PostgreSQL-specific options
uv run testdatagen generate postgres_example.tdg --format postgresql --output ./output \
  --pg-schema my_schema --pg-create-schema --pg-single-file
```

## PostgreSQL-specific Options

The following options are available for PostgreSQL export:

- `--pg-schema`: The PostgreSQL schema name (default: "public")
- `--pg-create-schema`: Include schema creation statements
- `--pg-single-file`: Export all tables to a single SQL file

## Example

The `postgres_example.tdg` file defines a simple e-commerce database with the following tables:

- `Customer`: Customer information
- `Product`: Product catalog
- `Order`: Customer orders
- `OrderItem`: Line items for each order

The generated SQL scripts will include:

1. Schema creation (if requested)
2. Table creation with appropriate PostgreSQL data types
3. Primary key, foreign key, unique, and check constraints
4. INSERT statements with generated test data

## Running the Generated SQL

The generated SQL scripts can be executed directly in PostgreSQL:

```bash
# Using psql
psql -U postgres -d your_database -f output/all_tables.sql

# Or individual files
psql -U postgres -d your_database -f output/schema.sql
psql -U postgres -d your_database -f output/Customer.sql
psql -U postgres -d your_database -f output/Product.sql
psql -U postgres -d your_database -f output/Order.sql
psql -U postgres -d your_database -f output/OrderItem.sql
```
