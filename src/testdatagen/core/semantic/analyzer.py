






from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel

from ..ast.nodes import ASTNode, SchemaNode, TableNode, FieldNode, ConstraintNode, TypeNode, NodeType
from ..types.registry import TypeRegistry, default_registry
from ..types.custom import CustomType
from .symbol_table import SymbolTable, Symbol
from .type_checker import TypeChecker, TypeCheckError


class SemanticError(BaseModel):
    """Represents a semantic error"""
    message: str
    line: int
    column: int
    severity: str = "error"  # "error", "warning", "info"


class SemanticAnalyzer:
    """Semantic analyzer for the DSL"""
    
    def __init__(self, type_registry: TypeRegistry = default_registry):
        self.symbol_table = SymbolTable()
        self.type_registry = type_registry
        self.type_checker = TypeChecker(self.symbol_table, type_registry)
        self.errors: List[SemanticError] = []
        
    def analyze(self, node: ASTNode) -> List[SemanticError]:
        """Analyze an AST node"""
        self.errors = []
        
        # Process schema node specially to handle type declarations first
        if isinstance(node, SchemaNode):
            # First, build symbols for the schema itself
            self.symbol_table.add_symbol(Symbol(
                name=node.name,
                kind="schema",
                source_line=node.line,
                source_column=node.column
            ))
            
            # Enter schema scope
            self.symbol_table.enter_scope(node.name)
            
            # Process types first - build symbols for all types
            for type_node in node.types:
                self._build_type_symbols(type_node)
            
            # Register custom types after building their symbols
            self._register_custom_types(node)
            
            # Now process tables after types are registered
            for table in node.tables:
                self._build_symbol_table(table)
                
            # Exit schema scope
            self.symbol_table.exit_scope()
        else:
            # For non-schema nodes, build symbol table normally
            self._build_symbol_table(node)
        
        # Check types
        type_errors = self.type_checker.check(node)
        
        # Convert type errors to semantic errors
        for error in type_errors:
            self.errors.append(SemanticError(
                message=error.message,
                line=error.node.line,
                column=error.node.column,
                severity=error.severity
            ))
        
        # Validate constraints
        self._validate_constraints(node)
        
        return self.errors
        
    def _register_custom_types(self, schema_node: SchemaNode) -> None:
        """Register custom types in the type registry"""
        # First, validate that all base types exist
        for type_node in schema_node.types:
            if not self.type_registry.exists(type_node.base_type):
                self.errors.append(SemanticError(
                    message=f"Unknown base type '{type_node.base_type}' for custom type '{type_node.name}'",
                    line=type_node.line,
                    column=type_node.column,
                    severity="error"
                ))
                continue
                
            # Check for duplicate type names
            if self.type_registry.exists(type_node.name):
                self.errors.append(SemanticError(
                    message=f"Type '{type_node.name}' is already defined",
                    line=type_node.line,
                    column=type_node.column,
                    severity="error"
                ))
                continue
                
        # Then register the types if they're valid
        for type_node in schema_node.types:
            # Skip registration if the base type doesn't exist or the type name is already taken
            if not self.type_registry.exists(type_node.base_type) or self.type_registry.exists(type_node.name):
                continue
                
            try:
                self.type_registry.register_custom_type_from_ast(type_node)
            except ValueError as e:
                self.errors.append(SemanticError(
                    message=str(e),
                    line=type_node.line,
                    column=type_node.column,
                    severity="error"
                ))
    
    def _build_symbol_table(self, node: ASTNode) -> None:
        """Build the symbol table from an AST node"""
        if node.node_type == NodeType.SCHEMA:
            self._build_schema_symbols(node)
        elif node.node_type == NodeType.TYPE:
            self._build_type_symbols(node)
        elif node.node_type == NodeType.TABLE:
            self._build_table_symbols(node)
        elif node.node_type == NodeType.FIELD:
            self._build_field_symbols(node)
        elif node.node_type == NodeType.CONSTRAINT:
            self._build_constraint_symbols(node)
    
    def _build_schema_symbols(self, node: SchemaNode) -> None:
        """Build symbols for a schema node"""
        # This method is now handled directly in the analyze method
        # to ensure proper ordering of type processing
        pass
    
    def _build_type_symbols(self, node: TypeNode) -> None:
        """Build symbols for a type node"""
        # Add type symbol
        self.symbol_table.add_symbol(Symbol(
            name=node.name,
            kind="type",
            type=node.base_type,
            attributes={
                "constraints": [c.name for c in node.constraints]
            },
            source_line=node.line,
            source_column=node.column
        ))
        
        # Process constraints
        for constraint in node.constraints:
            self._build_symbol_table(constraint)
    
    def _build_table_symbols(self, node: TableNode) -> None:
        """Build symbols for a table node"""
        # Add table symbol
        self.symbol_table.add_symbol(Symbol(
            name=node.name,
            kind="table",
            source_line=node.line,
            source_column=node.column
        ))
        
        # Enter table scope
        self.symbol_table.enter_scope(node.name)
        
        # Process fields
        for field in node.fields:
            self._build_symbol_table(field)
        
        # Process constraints
        for constraint in node.constraints:
            self._build_symbol_table(constraint)
        
        # Exit table scope
        self.symbol_table.exit_scope()
    
    def _build_field_symbols(self, node: FieldNode) -> None:
        """Build symbols for a field node"""
        # Add field symbol
        self.symbol_table.add_symbol(Symbol(
            name=node.name,
            kind="field",
            type=node.data_type,
            attributes={
                "nullable": node.nullable,
                "default_value": node.default_value
            },
            source_line=node.line,
            source_column=node.column
        ))
        
        # Process constraints
        for constraint in node.constraints:
            self._build_symbol_table(constraint)
    
    def _build_constraint_symbols(self, node: ConstraintNode) -> None:
        """Build symbols for a constraint node"""
        # Add constraint symbol
        self.symbol_table.add_symbol(Symbol(
            name=node.name,
            kind="constraint",
            type=node.constraint_type,
            attributes=node.parameters,
            source_line=node.line,
            source_column=node.column
        ))
    
    def _validate_constraints(self, node: ASTNode) -> None:
        """Validate constraints in an AST node"""
        if node.node_type == NodeType.SCHEMA:
            for table in node.tables:
                self._validate_constraints(table)
        elif node.node_type == NodeType.TABLE:
            # Validate table-level constraints
            for constraint in node.constraints:
                self._validate_table_constraint(constraint, node)
            
            # Validate field-level constraints
            for field in node.fields:
                for constraint in field.constraints:
                    self._validate_field_constraint(constraint, field)
    
    def _validate_table_constraint(self, constraint: ConstraintNode, table: TableNode) -> None:
        """Validate a table-level constraint"""
        # This would be expanded based on the specific constraint types
        # For now, just a placeholder
        pass
    
    def _validate_field_constraint(self, constraint: ConstraintNode, field: FieldNode) -> None:
        """Validate a field-level constraint"""
        # This would be expanded based on the specific constraint types
        # For now, just a placeholder
        pass
    
    def add_error(self, message: str, line: int, column: int, severity: str = "error") -> None:
        """Add a semantic error"""
        self.errors.append(SemanticError(
            message=message,
            line=line,
            column=column,
            severity=severity
        ))






