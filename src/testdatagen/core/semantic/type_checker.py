





from typing import Dict, List, Optional, Any, Union, Tuple
from pydantic import BaseModel

from ..ast.nodes import ASTNode, SchemaNode, TableNode, FieldNode, ConstraintNode, TypeNode
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
        elif isinstance(node, TypeNode):
            self._check_type(node)
        elif isinstance(node, TableNode):
            self._check_table(node)
        elif isinstance(node, FieldNode):
            self._check_field(node)
        elif isinstance(node, ConstraintNode):
            self._check_constraint(node)
        
        return self.errors
    
    def _check_schema(self, node: SchemaNode) -> None:
        """Check types in a schema node"""
        # Check for duplicate type names
        type_names = set()
        for type_node in node.types:
            if type_node.name in type_names:
                self.errors.append(TypeCheckError(
                    message=f"Duplicate type name: {type_node.name}",
                    node=type_node
                ))
            else:
                type_names.add(type_node.name)
            
            # Check each type
            self._check_type(type_node)
        
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
            
    def _check_type(self, node: TypeNode) -> None:
        """Check types in a type node"""
        # Check that the base type exists
        if not self.type_registry.exists(node.base_type):
            self.errors.append(TypeCheckError(
                message=f"Unknown base type: {node.base_type}",
                node=node
            ))
            return
            
        # Get the base type object
        base_type = self.type_registry.get(node.base_type)
        
        # Check for circular references
        if hasattr(base_type, 'base_type') and isinstance(base_type.base_type, str) and base_type.base_type == node.name:
            self.errors.append(TypeCheckError(
                message=f"Circular type reference detected: {node.name} -> {node.base_type} -> {node.name}",
                node=node
            ))
            return
            
        # Check constraints are compatible with the base type
        for constraint in node.constraints:
            self._check_constraint(constraint)
            self._check_constraint_compatibility_for_type(constraint, base_type, node)
            
    def _check_constraint_compatibility_for_type(self, constraint: ConstraintNode, base_type, type_node: TypeNode) -> None:
        """Check if a constraint is compatible with a type's base type"""
        constraint_type = constraint.constraint_type.lower()
        base_type_name = base_type.name
        
        # Check pattern constraints are only applied to string types
        if constraint_type == "pattern" and base_type_name != "string":
            self.errors.append(TypeCheckError(
                message=f"Pattern constraint can only be applied to string types, but custom type '{type_node.name}' has base type '{base_type_name}'",
                node=constraint
            ))
            
        # Check range constraints are only applied to numeric types
        if constraint_type == "range" and base_type_name not in ["integer", "decimal"]:
            self.errors.append(TypeCheckError(
                message=f"Range constraint can only be applied to numeric types, but custom type '{type_node.name}' has base type '{base_type_name}'",
                node=constraint
            ))
            
        # Check length constraints are only applied to string or array types
        if constraint_type == "length" and base_type_name not in ["string"] and not (hasattr(base_type, 'kind') and getattr(base_type, 'kind', None) == 'array'):
            self.errors.append(TypeCheckError(
                message=f"Length constraint can only be applied to string or array types, but custom type '{type_node.name}' has base type '{base_type_name}'",
                node=constraint
            ))
    
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
            return
            
        # Get the field's data type
        field_type = self.type_registry.get(node.data_type)
        
        # If it's a custom type, check that its base type exists
        if field_type and hasattr(field_type, 'base_type'):
            base_type = field_type.base_type
            if isinstance(base_type, str) and not self.type_registry.exists(base_type):
                self.errors.append(TypeCheckError(
                    message=f"Custom type '{node.data_type}' references unknown base type: {base_type}",
                    node=node
                ))
        
        # Check constraints
        for constraint in node.constraints:
            self._check_constraint(constraint)
            
        # Check if constraints are compatible with the field type
        self._check_constraint_compatibility(node, field_type)
        
    def _check_constraint_compatibility(self, field_node: FieldNode, field_type) -> None:
        """Check if constraints are compatible with the field type"""
        # Get the base type if it's a custom type
        base_type_name = field_type.name
        if hasattr(field_type, 'base_type'):
            base_type = field_type.base_type
            if isinstance(base_type, str):
                base_type_name = base_type
            elif hasattr(base_type, 'name'):
                base_type_name = base_type.name
        
        # Check each constraint for compatibility with the field type
        for constraint in field_node.constraints:
            constraint_type = constraint.constraint_type.lower()
            
            # Check pattern constraints are only applied to string types
            if constraint_type == "pattern" and base_type_name != "string":
                self.errors.append(TypeCheckError(
                    message=f"Pattern constraint can only be applied to string types, but field '{field_node.name}' has type '{field_type.name}'",
                    node=constraint
                ))
                
            # Check range constraints are only applied to numeric types
            if constraint_type == "range" and base_type_name not in ["integer", "decimal"]:
                self.errors.append(TypeCheckError(
                    message=f"Range constraint can only be applied to numeric types, but field '{field_node.name}' has type '{field_type.name}'",
                    node=constraint
                ))
    
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





