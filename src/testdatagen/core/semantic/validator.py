







from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel

from ..ast.nodes import ASTNode, SchemaNode, TableNode, FieldNode, ConstraintNode, TypeNode, NodeType
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
        elif node.node_type == NodeType.TYPE:
            self._validate_type(node)
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
        
        # Validate each type
        for type_node in node.types:
            self._validate_type(type_node)
        
        # Validate each table
        for table in node.tables:
            self._validate_table(table)
            
    def _validate_type(self, node: TypeNode) -> None:
        """Validate a type node"""
        # Check that the type has a valid base type
        from ..types.registry import default_registry
        
        # Validate the base type exists
        if not default_registry.exists(node.base_type):
            self.add_error(
                f"Base type '{node.base_type}' for custom type '{node.name}' does not exist",
                node.line,
                node.column,
                "error"
            )
            return
            
        # Get the base type object
        base_type_obj = default_registry.get(node.base_type)
        if not base_type_obj:
            return
            
        # Check for circular references in custom types
        if hasattr(base_type_obj, 'base_type'):
            visited_types = set([node.name])
            current_type = base_type_obj
            
            while hasattr(current_type, 'base_type') and isinstance(current_type.base_type, str):
                base_type_name = current_type.base_type
                
                if base_type_name in visited_types:
                    self.add_error(
                        f"Circular type reference detected in type chain for '{node.name}'",
                        node.line,
                        node.column,
                        "error"
                    )
                    return
                    
                visited_types.add(base_type_name)
                current_type = default_registry.get(base_type_name)
                if not current_type:
                    break
            
        # Validate constraints are appropriate for the base type
        for constraint in node.constraints:
            self._validate_constraint_for_type(constraint, base_type_obj, node)
            
        # Validate that the type has at least one constraint or is different from its base type
        if not node.constraints:
            self.add_error(
                f"Custom type '{node.name}' is identical to its base type '{node.base_type}'. Consider adding constraints or using the base type directly.",
                node.line,
                node.column,
                "warning"
            )
                
    def _validate_constraint_for_type(self, constraint: ConstraintNode, base_type, type_node: TypeNode) -> None:
        """Validate that a constraint is appropriate for a type"""
        constraint_type = constraint.constraint_type.lower()
        
        # Check pattern constraints are only applied to string types
        if constraint_type == "pattern" and base_type.name != "string":
            self.add_error(
                f"Pattern constraint can only be applied to string types, but '{type_node.name}' has base type '{base_type.name}'",
                constraint.line,
                constraint.column,
                "error"
            )
            
        # Check range constraints are only applied to numeric types
        if constraint_type == "range" and base_type.name not in ["integer", "decimal"]:
            self.add_error(
                f"Range constraint can only be applied to numeric types, but '{type_node.name}' has base type '{base_type.name}'",
                constraint.line,
                constraint.column,
                "error"
            )
    
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
        # Check that the data type exists
        from ..types.registry import default_registry
        
        if not default_registry.exists(node.data_type):
            self.add_error(
                f"Unknown data type '{node.data_type}' for field '{node.name}'",
                node.line,
                node.column,
                "error"
            )
            return
            
        # Get the field's data type
        field_type = default_registry.get(node.data_type)
        
        # If it's a custom type, check that its constraints don't conflict with field constraints
        if field_type and hasattr(field_type, 'constraints') and field_type.constraints:
            # Check for constraint conflicts between custom type and field
            type_constraint_types = set(c.get('type', '').lower() for c in field_type.constraints)
            field_constraint_types = set(c.constraint_type.lower() for c in node.constraints)
            
            # Find overlapping constraint types
            overlapping = type_constraint_types.intersection(field_constraint_types)
            if overlapping:
                self.add_error(
                    f"Field '{node.name}' has constraints that may conflict with its custom type '{node.data_type}': {', '.join(overlapping)}",
                    node.line,
                    node.column,
                    "warning"
                )
        
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







