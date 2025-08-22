



















from typing import Dict, List, Optional, Any, Union, Tuple
import random
import string
import uuid
import datetime
import json
import pandas as pd
import numpy as np

from ...core.ast.nodes import SchemaNode, TableNode, FieldNode
from .base import GenerationStrategy


class RandomStrategy(GenerationStrategy):
    """Strategy for generating random data"""
    
    def __init__(self):
        super().__init__()
        self.random = random.Random()
    
    def initialize(self, schema: SchemaNode, options: Dict[str, Any]) -> None:
        """Initialize the strategy with a schema and options"""
        super().initialize(schema, options)
        
        # Set random seed if provided
        if "seed" in options and options["seed"] is not None:
            self.random.seed(options["seed"])
    
    def generate_table(self, table: TableNode, options: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Generate data for a table"""
        # Get record count
        record_count = options.get("record_count", 100)
        
        # Generate data
        data = []
        
        # Measure execution time
        def generate_data():
            for i in range(record_count):
                row = {}
                for field in table.fields:
                    row[field.name] = self.generate_field(field, table, i, {})
                data.append(row)
            return pd.DataFrame(data)
        
        df, execution_time_ms = self.measure_execution_time(generate_data)
        
        # Collect statistics
        stats = {
            "record_count": record_count,
            "generation_time_ms": execution_time_ms,
            "avg_time_per_record_ms": execution_time_ms / record_count if record_count > 0 else 0
        }
        
        return df, stats
    
    def generate_field(self, field: FieldNode, table: TableNode, row_index: int, context: Dict[str, Any]) -> Any:
        """Generate a value for a field"""
        # Check if field is nullable and randomly decide to return None
        if field.nullable and self.random.random() < 0.1:  # 10% chance of NULL
            return None
        
        # Generate based on data type
        data_type = field.data_type.lower()
        
        if data_type == "integer":
            return self._generate_integer(field)
        elif data_type == "decimal":
            return self._generate_decimal(field)
        elif data_type == "string":
            return self._generate_string(field)
        elif data_type == "boolean":
            return self._generate_boolean(field)
        elif data_type == "date":
            return self._generate_date(field)
        elif data_type == "timestamp":
            return self._generate_timestamp(field)
        elif data_type == "binary":
            return self._generate_binary(field)
        elif data_type == "uuid":
            return self._generate_uuid(field)
        elif data_type == "json":
            return self._generate_json(field)
        elif "[]" in data_type:  # Array type
            return self._generate_array(field)
        else:
            # Unknown type, return None
            return None
    
    def _generate_integer(self, field: FieldNode) -> int:
        """Generate a random integer"""
        # Check for range constraints
        min_value = -1000000
        max_value = 1000000
        
        for constraint in field.constraints:
            if constraint.constraint_type == "range":
                if "min_value" in constraint.parameters:
                    min_value = constraint.parameters["min_value"]
                if "max_value" in constraint.parameters:
                    max_value = constraint.parameters["max_value"]
        
        return self.random.randint(min_value, max_value)
    
    def _generate_decimal(self, field: FieldNode) -> float:
        """Generate a random decimal"""
        # Check for range constraints
        min_value = -1000000.0
        max_value = 1000000.0
        
        for constraint in field.constraints:
            if constraint.constraint_type == "range":
                if "min_value" in constraint.parameters:
                    min_value = constraint.parameters["min_value"]
                if "max_value" in constraint.parameters:
                    max_value = constraint.parameters["max_value"]
        
        return min_value + self.random.random() * (max_value - min_value)
    
    def _generate_string(self, field: FieldNode) -> str:
        """Generate a random string"""
        # Check for length constraints
        min_length = 5
        max_length = 20
        
        for constraint in field.constraints:
            if constraint.constraint_type == "length":
                if "min_length" in constraint.parameters:
                    min_length = constraint.parameters["min_length"]
                if "max_length" in constraint.parameters:
                    max_length = constraint.parameters["max_length"]
        
        # Generate random length
        length = self.random.randint(min_length, max_length)
        
        # Generate random string
        chars = string.ascii_letters + string.digits
        return ''.join(self.random.choice(chars) for _ in range(length))
    
    def _generate_boolean(self, field: FieldNode) -> bool:
        """Generate a random boolean"""
        return self.random.choice([True, False])
    
    def _generate_date(self, field: FieldNode) -> str:
        """Generate a random date"""
        # Generate a date between 1970 and 2030
        start_date = datetime.date(1970, 1, 1)
        end_date = datetime.date(2030, 12, 31)
        days_between = (end_date - start_date).days
        random_days = self.random.randint(0, days_between)
        random_date = start_date + datetime.timedelta(days=random_days)
        return random_date.isoformat()
    
    def _generate_timestamp(self, field: FieldNode) -> str:
        """Generate a random timestamp"""
        # Generate a timestamp between 1970 and 2030
        start_date = datetime.datetime(1970, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(2030, 12, 31, 23, 59, 59)
        seconds_between = int((end_date - start_date).total_seconds())
        random_seconds = self.random.randint(0, seconds_between)
        random_timestamp = start_date + datetime.timedelta(seconds=random_seconds)
        return random_timestamp.isoformat()
    
    def _generate_binary(self, field: FieldNode) -> bytes:
        """Generate random binary data"""
        # Generate random bytes
        length = self.random.randint(10, 100)
        return bytes(self.random.randint(0, 255) for _ in range(length))
    
    def _generate_uuid(self, field: FieldNode) -> str:
        """Generate a random UUID"""
        return str(uuid.uuid4())
    
    def _generate_json(self, field: FieldNode) -> Dict[str, Any]:
        """Generate random JSON data"""
        # Generate a simple JSON object
        keys = [self._generate_string(field) for _ in range(self.random.randint(1, 5))]
        values = [
            self.random.choice([
                self._generate_string(field),
                self._generate_integer(field),
                self._generate_boolean(field),
                [self._generate_string(field) for _ in range(self.random.randint(1, 3))]
            ])
            for _ in range(len(keys))
        ]
        return dict(zip(keys, values))
    
    def _generate_array(self, field: FieldNode) -> List[Any]:
        """Generate a random array"""
        # Extract base type from array type (e.g., "string[]" -> "string")
        base_type = field.data_type.split("[")[0]
        
        # Create a temporary field with the base type
        temp_field = FieldNode(
            node_type=field.node_type,
            name=field.name,
            data_type=base_type,
            constraints=field.constraints,
            nullable=field.nullable,
            line=field.line,
            column=field.column
        )
        
        # Generate array elements
        length = self.random.randint(0, 5)
        return [self.generate_field(temp_field, None, i, {}) for i in range(length)]



















