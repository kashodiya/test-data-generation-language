







from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel

from ..ast.nodes import ASTNode, SchemaNode, TableNode, FieldNode, ConstraintNode, NodeType
from ..constraints.base import Constraint, ConstraintViolation
from .analyzer import SemanticAnalyzer, SemanticError


class ValidationError(BaseModel):
    """Represents a validation error"""
    message: str
    line: int
    column: int
    severity: str = "error"  # "error", "warning", "info"


class Validator:
    """Validator for the DSL"""
    
    def __init__(self, analyzer: Optional[SemanticAnalyzer] = None):
        self.analyzer = analyzer or SemanticAnalyzer()
        self.errors: List[ValidationError] = []
        
    def validate(self, node: ASTNode) -> List[ValidationError]:
        """Validate an AST node"""
        self.errors = []
        
        # First, perform semantic analysis
        semantic_errors = self.analyzer.analyze(node)
        
        # Convert semantic errors to validation errors
        for error in semantic_errors:
            self.errors.append(ValidationError(
                message=error.message,
                line=error.line,
                column=error.column,
                severity=error.severity
            ))
        
        # If there are semantic errors, don't proceed with validation
        if self.errors:
            return self.errors
        
        # Validate the node
        if node.node_type == NodeType.SCHEMA:
            self._validate_schema(node)
        elif node.node_type == NodeType.TABLE:
            self._validate_table(node)
        elif node.node_type == NodeType.FIELD:
            self._validate_field(node)
        
        return self.errors
    
    def _validate_schema(self, node: SchemaNode) -> None:
        """Validate a schema node"""
        # Check that the schema has at least one table
        if not node.tables:
            self.add_error("Schema must have at least one table", node.line, node.column, "warning")
        
        # Validate each table
        for table in node.tables:
            self._validate_table(table)
    
    def _validate_table(self, node: TableNode) -> None:
        """Validate a table node"""
        # Check that the table has at least one field
        if not node.fields:
            self.add_error(f"Table '{node.name}' must have at least one field", node.line, node.column, "error")
        
        # Check for primary key
        has_primary_key = False
        for constraint in node.constraints:
            if constraint.constraint_type == "primary_key":
                has_primary_key = True
                break
        
        if not has_primary_key:
            self.add_error(f"Table '{node.name}' should have a primary key", node.line, node.column, "warning")
        
        # Validate each field
        for field in node.fields:
            self._validate_field(field)
    
    def _validate_field(self, node: FieldNode) -> None:
        """Validate a field node"""
        # Check for conflicting constraints
        self._check_conflicting_constraints(node)
    
    def _check_conflicting_constraints(self, node: FieldNode) -> None:
        """Check for conflicting constraints on a field"""
        # Example: Check for both NULL and NOT NULL constraints
        has_null = False
        has_not_null = False
        
        for constraint in node.constraints:
            if constraint.constraint_type == "null":
                has_null = True
            elif constraint.constraint_type == "not_null":
                has_not_null = True
        
        if has_null and has_not_null:
            self.add_error(f"Field '{node.name}' has conflicting NULL and NOT NULL constraints", node.line, node.column, "error")
    
    def add_error(self, message: str, line: int, column: int, severity: str = "error") -> None:
        """Add a validation error"""
        self.errors.append(ValidationError(
            message=message,
            line=line,
            column=column,
            severity=severity
        ))







