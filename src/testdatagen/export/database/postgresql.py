import os
from typing import Dict, List, Optional, Any, Union
import pandas as pd
import datetime
import uuid

from ..base import Exporter


class PostgreSQLExporter(Exporter):
    """Exporter for PostgreSQL database format"""
    
    # Mapping of TDG types to PostgreSQL types
    TYPE_MAPPING = {
        "integer": "INTEGER",
        "decimal": "NUMERIC",
        "string": "VARCHAR(255)",
        "boolean": "BOOLEAN",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "binary": "BYTEA",
        "uuid": "UUID",
        "json": "JSONB"
    }
    
    def export(self, data: pd.DataFrame, output_path: str, **options) -> None:
        """
        Export data to a PostgreSQL SQL script
        
        Args:
            data: The data to export
            output_path: The path to write the output to
            **options: Additional options for the exporter
                - table_name: The name of the table
                - schema_name: The PostgreSQL schema name (default: public)
                - create_table: Whether to include CREATE TABLE statement (default: True)
                - drop_table: Whether to include DROP TABLE statement (default: False)
                - column_types: Dict mapping column names to PostgreSQL data types
                - primary_key: Column or list of columns to use as primary key
                - foreign_keys: Dict of column to (table, column) for foreign keys
                - unique_constraints: List of columns or column lists with unique constraints
                - check_constraints: Dict of constraint names to check expressions
                - transaction: Whether to wrap in a transaction (default: True)
                - batch_size: Number of rows per INSERT statement (default: 1000)
        """
        # Get options
        table_name = options.get("table_name", "table")
        schema_name = options.get("schema_name", "public")
        create_table = options.get("create_table", True)
        drop_table = options.get("drop_table", False)
        column_types = options.get("column_types", {})
        primary_key = options.get("primary_key", None)
        foreign_keys = options.get("foreign_keys", {})
        unique_constraints = options.get("unique_constraints", [])
        check_constraints = options.get("check_constraints", {})
        transaction = options.get("transaction", True)
        batch_size = options.get("batch_size", 1000)
        
        # Generate SQL
        sql_parts = []
        
        # Start transaction if requested
        if transaction:
            sql_parts.append("BEGIN;")
        
        # Drop table if requested
        if drop_table:
            sql_parts.append(f"DROP TABLE IF EXISTS {schema_name}.{table_name};")
        
        # Create table if requested
        if create_table:
            create_sql = self._generate_create_table(
                data, 
                table_name, 
                schema_name, 
                column_types, 
                primary_key, 
                foreign_keys, 
                unique_constraints, 
                check_constraints
            )
            sql_parts.append(create_sql)
        
        # Generate INSERT statements
        insert_statements = self._generate_insert_statements(
            data, 
            table_name, 
            schema_name, 
            batch_size
        )
        sql_parts.extend(insert_statements)
        
        # Commit transaction if requested
        if transaction:
            sql_parts.append("COMMIT;")
        
        # Write to file
        with open(output_path, "w") as f:
            f.write("\n\n".join(sql_parts))
    
    def export_all(self, data: Dict[str, pd.DataFrame], output_dir: str, **options) -> Dict[str, str]:
        """
        Export multiple datasets to PostgreSQL SQL scripts
        
        Args:
            data: A dictionary of table names to DataFrames
            output_dir: The directory to write the output to
            **options: Additional options for the exporter
                - file_suffix: The suffix to add to file names, default '.sql'
                - schema_name: The PostgreSQL schema name (default: public)
                - create_schema: Whether to create the schema (default: True)
                - drop_schema: Whether to drop the schema first (default: False)
                - create_tables: Whether to include CREATE TABLE statements (default: True)
                - drop_tables: Whether to include DROP TABLE statements (default: False)
                - column_types: Dict mapping table.column to PostgreSQL data types
                - primary_keys: Dict mapping table names to primary key column(s)
                - foreign_keys: Dict mapping table.column to (table, column) for foreign keys
                - unique_constraints: Dict mapping table names to lists of unique constraints
                - check_constraints: Dict mapping table names to dicts of check constraints
                - single_file: Whether to output a single SQL file (default: False)
                - transaction: Whether to wrap in a transaction (default: True)
                - batch_size: Number of rows per INSERT statement (default: 1000)
            
        Returns:
            A dictionary of table names to output file paths
        """
        # Get options
        file_suffix = options.get("file_suffix", ".sql")
        schema_name = options.get("schema_name", "public")
        create_schema = options.get("create_schema", True)
        drop_schema = options.get("drop_schema", False)
        create_tables = options.get("create_tables", True)
        drop_tables = options.get("drop_tables", False)
        column_types = options.get("column_types", {})
        primary_keys = options.get("primary_keys", {})
        foreign_keys = options.get("foreign_keys", {})
        unique_constraints = options.get("unique_constraints", {})
        check_constraints = options.get("check_constraints", {})
        single_file = options.get("single_file", False)
        transaction = options.get("transaction", True)
        batch_size = options.get("batch_size", 1000)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        if single_file:
            # Export all tables to a single file
            output_path = os.path.join(output_dir, f"all_tables{file_suffix}")
            
            with open(output_path, "w") as f:
                # Start transaction if requested
                if transaction:
                    f.write("BEGIN;\n\n")
                
                # Drop schema if requested
                if drop_schema:
                    f.write(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;\n\n")
                
                # Create schema if requested
                if create_schema:
                    f.write(f"CREATE SCHEMA IF NOT EXISTS {schema_name};\n\n")
                
                # Process each table in dependency order
                for table_name, df in data.items():
                    # Get table-specific options
                    table_column_types = {col: column_types.get(f"{table_name}.{col}", None) 
                                         for col in df.columns}
                    table_primary_key = primary_keys.get(table_name, None)
                    table_foreign_keys = {col: foreign_keys.get(f"{table_name}.{col}", None) 
                                         for col in df.columns}
                    table_unique = unique_constraints.get(table_name, [])
                    table_checks = check_constraints.get(table_name, {})
                    
                    # Drop table if requested
                    if drop_tables:
                        f.write(f"DROP TABLE IF EXISTS {schema_name}.{table_name};\n\n")
                    
                    # Create table
                    if create_tables:
                        create_sql = self._generate_create_table(
                            df, 
                            table_name, 
                            schema_name, 
                            table_column_types, 
                            table_primary_key, 
                            table_foreign_keys, 
                            table_unique, 
                            table_checks
                        )
                        f.write(create_sql + "\n\n")
                    
                    # Generate INSERT statements
                    insert_statements = self._generate_insert_statements(
                        df, 
                        table_name, 
                        schema_name, 
                        batch_size
                    )
                    f.write("\n".join(insert_statements) + "\n\n")
                
                # Commit transaction if requested
                if transaction:
                    f.write("COMMIT;\n")
            
            return {"all_tables": output_path}
        else:
            # Export each table to a separate file
            result = {}
            for table_name, df in data.items():
                output_path = os.path.join(output_dir, f"{table_name}{file_suffix}")
                
                # Get table-specific options
                table_options = options.copy()
                table_options["table_name"] = table_name
                table_options["schema_name"] = schema_name
                table_options["create_table"] = create_tables
                table_options["drop_table"] = drop_tables
                
                # Extract table-specific constraints
                table_options["column_types"] = {col: column_types.get(f"{table_name}.{col}", None) 
                                               for col in df.columns}
                table_options["primary_key"] = primary_keys.get(table_name, None)
                table_options["foreign_keys"] = {col: foreign_keys.get(f"{table_name}.{col}", None) 
                                               for col in df.columns}
                table_options["unique_constraints"] = unique_constraints.get(table_name, [])
                table_options["check_constraints"] = check_constraints.get(table_name, {})
                
                # Export table
                self.export(df, output_path, **table_options)
                result[table_name] = output_path
            
            # If schema creation/dropping is requested, create a separate file for it
            if create_schema or drop_schema:
                schema_path = os.path.join(output_dir, f"00_schema{file_suffix}")
                with open(schema_path, "w") as f:
                    if transaction:
                        f.write("BEGIN;\n\n")
                    
                    if drop_schema:
                        f.write(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;\n\n")
                    
                    if create_schema:
                        f.write(f"CREATE SCHEMA IF NOT EXISTS {schema_name};\n\n")
                    
                    if transaction:
                        f.write("COMMIT;\n")
                
                result["schema"] = schema_path
            
            return result
    
    def _generate_create_table(
        self, 
        data: pd.DataFrame, 
        table_name: str, 
        schema_name: str, 
        column_types: Dict[str, str], 
        primary_key: Union[str, List[str], None], 
        foreign_keys: Dict[str, tuple], 
        unique_constraints: List[Union[str, List[str]]], 
        check_constraints: Dict[str, str]
    ) -> str:
        """Generate CREATE TABLE statement"""
        # Start CREATE TABLE statement
        sql = f"CREATE TABLE {schema_name}.{table_name} (\n"
        
        # Add columns
        column_defs = []
        for column in data.columns:
            # Determine column type
            if column in column_types and column_types[column]:
                col_type = column_types[column]
            else:
                col_type = self._infer_column_type(data[column])
            
            # Add column definition
            column_defs.append(f"    {column} {col_type}")
        
        # Add primary key constraint if specified
        if primary_key:
            if isinstance(primary_key, str):
                primary_key = [primary_key]
            pk_columns = ", ".join(primary_key)
            column_defs.append(f"    PRIMARY KEY ({pk_columns})")
        
        # Add foreign key constraints
        for column, reference in foreign_keys.items():
            if reference:
                ref_table, ref_column = reference
                column_defs.append(
                    f"    FOREIGN KEY ({column}) REFERENCES {schema_name}.{ref_table}({ref_column})"
                )
        
        # Add unique constraints
        for constraint in unique_constraints:
            if isinstance(constraint, str):
                constraint = [constraint]
            columns = ", ".join(constraint)
            column_defs.append(f"    UNIQUE ({columns})")
        
        # Add check constraints
        for name, expression in check_constraints.items():
            column_defs.append(f"    CONSTRAINT {name} CHECK ({expression})")
        
        # Combine all column definitions
        sql += ",\n".join(column_defs)
        
        # Close CREATE TABLE statement
        sql += "\n);"
        
        return sql
    
    def _generate_insert_statements(
        self, 
        data: pd.DataFrame, 
        table_name: str, 
        schema_name: str, 
        batch_size: int
    ) -> List[str]:
        """Generate INSERT statements for the data"""
        if data.empty:
            return []
        
        statements = []
        
        # Process data in batches
        for i in range(0, len(data), batch_size):
            batch = data.iloc[i:i+batch_size]
            
            # Start INSERT statement
            columns = ", ".join(batch.columns)
            sql = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES\n"
            
            # Add values
            values = []
            for _, row in batch.iterrows():
                value_list = []
                for col in batch.columns:
                    value = row[col]
                    value_list.append(self._format_value(value))
                
                values.append(f"    ({', '.join(value_list)})")
            
            sql += ",\n".join(values) + ";"
            statements.append(sql)
        
        return statements
    
    def _infer_column_type(self, series: pd.Series) -> str:
        """Infer PostgreSQL column type from pandas Series"""
        dtype = series.dtype
        
        # Check for numeric types
        if pd.api.types.is_integer_dtype(dtype):
            return "INTEGER"
        elif pd.api.types.is_float_dtype(dtype):
            return "NUMERIC"
        
        # Check for boolean
        elif pd.api.types.is_bool_dtype(dtype):
            return "BOOLEAN"
        
        # Check for datetime types
        elif pd.api.types.is_datetime64_dtype(dtype):
            return "TIMESTAMP"
        elif pd.api.types.is_datetime64_ns_dtype(dtype):
            return "TIMESTAMP"
        
        # Check for string types
        elif pd.api.types.is_string_dtype(dtype):
            # Check if all values are UUIDs
            if not series.empty and all(self._is_uuid(val) for val in series.dropna()):
                return "UUID"
            
            # Check if all values are JSON
            if not series.empty and all(self._is_json(val) for val in series.dropna()):
                return "JSONB"
            
            # Default to VARCHAR
            try:
                # Try to get max length if all values are strings
                max_length = series.str.len().max() if not series.empty else 255
                return f"VARCHAR({max(max_length, 255)})"
            except (AttributeError, TypeError):
                # If we can't get string length, use TEXT
                return "TEXT"
        
        # Default to TEXT for unknown types
        return "TEXT"
    
    def _format_value(self, value: Any) -> str:
        """Format a value for SQL INSERT statement"""
        if value is None or pd.isna(value):
            return "NULL"
        
        # Handle different types
        if isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        elif isinstance(value, (datetime.date, datetime.datetime)):
            return f"'{value.isoformat()}'"
        elif isinstance(value, (list, dict)):
            import json
            return f"'{json.dumps(value)}'::jsonb"
        elif isinstance(value, uuid.UUID):
            return f"'{str(value)}'"
        else:
            # Escape single quotes for strings
            escaped_val = str(value).replace("'", "''")
            return f"'{escaped_val}'"
    
    def _is_uuid(self, value: Any) -> bool:
        """Check if a value is a UUID"""
        if not isinstance(value, str):
            return False
        
        try:
            uuid.UUID(value)
            return True
        except (ValueError, AttributeError, TypeError):
            return False
    
    def _is_json(self, value: Any) -> bool:
        """Check if a value is JSON"""
        if isinstance(value, (dict, list)):
            return True
        
        if not isinstance(value, str):
            return False
        
        try:
            import json
            json.loads(value)
            return True
        except (ValueError, TypeError):
            return False
