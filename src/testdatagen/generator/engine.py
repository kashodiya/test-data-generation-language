















from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel
import pandas as pd

from ..core.ast.nodes import SchemaNode, TableNode, FieldNode
from .strategies.base import GenerationStrategy


class GenerationOptions(BaseModel):
    """Options for data generation"""
    record_count: int = 100
    batch_size: int = 1000
    seed: Optional[int] = None
    locale: str = "en_US"
    strategy: str = "random"
    strategy_options: Dict[str, Any] = {}


class GenerationResult(BaseModel):
    """Result of data generation"""
    data: Dict[str, Any]
    stats: Dict[str, Any]
    success: bool
    errors: List[str] = []


class GenerationEngine:
    """Engine for generating test data"""
    
    def __init__(self, strategies: Dict[str, GenerationStrategy]):
        self.strategies = strategies
    
    def generate(self, schema: SchemaNode, options: GenerationOptions) -> GenerationResult:
        """Generate test data for a schema"""
        try:
            # Select strategy
            strategy = self.strategies.get(options.strategy)
            if not strategy:
                return GenerationResult(
                    data={},
                    stats={},
                    success=False,
                    errors=[f"Unknown strategy: {options.strategy}"]
                )
            
            # Initialize strategy
            strategy.initialize(schema, options)
            
            # Generate data for each table
            data = {}
            stats = {
                "total_records": 0,
                "generation_time_ms": 0,
                "tables": {}
            }
            
            # Determine generation order based on dependencies
            tables = self._determine_generation_order(schema)
            
            # Generate data for each table
            for table in tables:
                table_data, table_stats = strategy.generate_table(table, options)
                data[table.name] = table_data
                stats["tables"][table.name] = table_stats
                stats["total_records"] += table_stats.get("record_count", 0)
                stats["generation_time_ms"] += table_stats.get("generation_time_ms", 0)
            
            return GenerationResult(
                data=data,
                stats=stats,
                success=True
            )
        except Exception as e:
            return GenerationResult(
                data={},
                stats={},
                success=False,
                errors=[f"Error generating data: {str(e)}"]
            )
    
    def _determine_generation_order(self, schema: SchemaNode) -> List[TableNode]:
        """
        Determine the order in which tables should be generated
        based on foreign key dependencies
        """
        # Build dependency graph
        dependencies = {}
        for table in schema.tables:
            dependencies[table.name] = set()
            
            # Check table constraints for foreign keys
            for constraint in table.constraints:
                if constraint.constraint_type == "foreign_key":
                    target_table = constraint.parameters.get("target_table")
                    if target_table:
                        dependencies[table.name].add(target_table)
        
        # Topological sort
        visited = set()
        temp_visited = set()
        order = []
        
        def visit(table_name):
            if table_name in temp_visited:
                # Cyclic dependency
                raise ValueError(f"Cyclic dependency detected involving table {table_name}")
            
            if table_name not in visited:
                temp_visited.add(table_name)
                
                # Visit dependencies
                for dep in dependencies.get(table_name, set()):
                    visit(dep)
                
                temp_visited.remove(table_name)
                visited.add(table_name)
                
                # Add to order
                table = next((t for t in schema.tables if t.name == table_name), None)
                if table:
                    order.append(table)
        
        # Visit all tables
        for table in schema.tables:
            if table.name not in visited:
                visit(table.name)
        
        return order















