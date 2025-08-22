





from typing import Dict, List, Optional, Any, Union, Tuple
from pydantic import BaseModel

from ..ast.nodes import ASTNode, SchemaNode, TableNode, FieldNode, ConstraintNode
from ..types.registry import TypeRegistry, default_registry
from .symbol_table import SymbolTable, Symbol


class TypeCheckError(BaseModel):
    """Represents a type checking error"""
    message: str
    node: ASTNode
    severity: str = "error"  # "error", "warning", "info"


class TypeChecker:
    """Type checker for the DSL"""
    
    def __init__(self, symbol_table: SymbolTable, type_registry: TypeRegistry = default_registry):
        self.symbol_table = symbol_table
        self.type_registry = type_registry
        self.errors: List[TypeCheckError] = []
        
    def check(self, node: ASTNode) -> List[TypeCheckError]:
        """Check types in an AST node"""
        self.errors = []
        
        if isinstance(node, SchemaNode):
            self._check_schema(node)
        elif isinstance(node, TableNode):
            self._check_table(node)
        elif isinstance(node, FieldNode):
            self._check_field(node)
        elif isinstance(node, ConstraintNode):
            self._check_constraint(node)
        
        return self.errors
    
    def _check_schema(self, node: SchemaNode) -> None:
        """Check types in a schema node"""
        # Check for duplicate table names
        table_names = set()
        for table in node.tables:
            if table.name in table_names:
                self.errors.append(TypeCheckError(
                    message=f"Duplicate table name: {table.name}",
                    node=table
                ))
            else:
                table_names.add(table.name)
            
            # Check each table
            self._check_table(table)
    
    def _check_table(self, node: TableNode) -> None:
        """Check types in a table node"""
        # Check for duplicate field names
        field_names = set()
        for field in node.fields:
            if field.name in field_names:
                self.errors.append(TypeCheckError(
                    message=f"Duplicate field name: {field.name}",
                    node=field
                ))
            else:
                field_names.add(field.name)
            
            # Check each field
            self._check_field(field)
        
        # Check constraints
        for constraint in node.constraints:
            self._check_constraint(constraint)
    
    def _check_field(self, node: FieldNode) -> None:
        """Check types in a field node"""
        # Check that the data type exists
        if not self.type_registry.exists(node.data_type):
            self.errors.append(TypeCheckError(
                message=f"Unknown data type: {node.data_type}",
                node=node
            ))
        
        # Check constraints
        for constraint in node.constraints:
            self._check_constraint(constraint)
    
    def _check_constraint(self, node: ConstraintNode) -> None:
        """Check types in a constraint node"""
        # This would be expanded based on the specific constraint types
        # For now, just a placeholder
        pass
    
    def _check_expression_types(self, expression: str, expected_type: str, context: Dict[str, str]) -> bool:
        """
        Check types in an expression
        
        Args:
            expression: The expression to check
            expected_type: The expected result type
            context: A mapping of variable names to their types
            
        Returns:
            True if the expression type matches the expected type, False otherwise
        """
        # This would require an expression type checker
        # For now, just a placeholder that always succeeds
        return True
    
    def add_error(self, message: str, node: ASTNode, severity: str = "error") -> None:
        """Add a type checking error"""
        self.errors.append(TypeCheckError(
            message=message,
            node=node,
            severity=severity
        ))





