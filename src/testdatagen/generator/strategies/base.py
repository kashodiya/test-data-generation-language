

















from typing import Dict, List, Optional, Any, Union, Tuple
from abc import ABC, abstractmethod
import time
import pandas as pd

from ...core.ast.nodes import SchemaNode, TableNode, FieldNode


class GenerationStrategy(ABC):
    """Base class for data generation strategies"""
    
    def __init__(self):
        self.schema = None
        self.options = None
        self.context = {}
    
    def initialize(self, schema: SchemaNode, options: Any) -> None:
        """Initialize the strategy with a schema and options"""
        self.schema = schema
        self.options = options
        self.context = {}
    
    @abstractmethod
    def generate_table(self, table: TableNode, options: Any) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Generate data for a table
        
        Args:
            table: The table to generate data for
            options: Generation options
            
        Returns:
            A tuple of (DataFrame with generated data, statistics)
        """
        pass
    
    @abstractmethod
    def generate_field(self, field: FieldNode, table: TableNode, row_index: int, context: Dict[str, Any]) -> Any:
        """
        Generate a value for a field
        
        Args:
            field: The field to generate a value for
            table: The table the field belongs to
            row_index: The index of the current row
            context: Generation context
            
        Returns:
            A generated value for the field
        """
        pass
    
    def get_table_by_name(self, table_name: str) -> Optional[TableNode]:
        """Get a table by name"""
        if not self.schema:
            return None
            
        for table in self.schema.tables:
            if table.name == table_name:
                return table
                
        return None
    
    def get_field_by_name(self, table: TableNode, field_name: str) -> Optional[FieldNode]:
        """Get a field by name"""
        for field in table.fields:
            if field.name == field_name:
                return field
                
        return None
    
    def measure_execution_time(self, func, *args, **kwargs) -> Tuple[Any, float]:
        """
        Measure the execution time of a function
        
        Args:
            func: The function to measure
            *args, **kwargs: Arguments to pass to the function
            
        Returns:
            A tuple of (function result, execution time in milliseconds)
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time_ms = (end_time - start_time) * 1000
        return result, execution_time_ms

















