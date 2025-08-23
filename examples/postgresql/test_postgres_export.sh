#!/bin/bash

# Test script for PostgreSQL export feature

# Create output directory
mkdir -p ./output

# Generate PostgreSQL SQL script from example schema
echo "Generating PostgreSQL SQL script from example schema..."
uv run testdatagen generate postgres_example.tdg --format postgresql --output ./output --pg-schema test_data --pg-create-schema --pg-single-file

echo "Done! SQL script generated at ./output/all_tables.sql"
echo ""
echo "To run this SQL script in PostgreSQL:"
echo "  psql -U postgres -d your_database -f ./output/all_tables.sql"
echo ""
echo "Or you can view the generated SQL:"
echo "  head -n 50 ./output/all_tables.sql"
