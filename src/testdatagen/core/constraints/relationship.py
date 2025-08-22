




from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

from .base import Constraint, ConstraintType


class RelationshipConstraint(Constraint):
    """Base class for relationship constraints"""
    constraint_type: ConstraintType = ConstraintType.RELATIONSHIP


class ForeignKeyConstraint(RelationshipConstraint):
    """Constraint for foreign key relationships"""
    source_fields: List[str]  # Fields in the source table
    target_table: str  # Name of the target table
    target_fields: List[str]  # Fields in the target table
    on_delete: Optional[str] = None  # Action to take when parent is deleted (CASCADE, SET NULL, etc.)
    on_update: Optional[str] = None  # Action to take when parent is updated
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate that a foreign key reference is valid
        
        Note: This requires:
        - 'reference_resolver' in the context to check references
        - 'field_values' dict with values for all source fields
        """
        if value is None:
            return True
            
        resolver = context.get('reference_resolver')
        if not resolver:
            raise ValueError("Reference resolver not provided in context")
            
        field_values = context.get('field_values', {})
        
        # Extract values for all source fields
        source_values = [field_values.get(field) for field in self.source_fields]
        
        # Check if any source value is None (unless we're validating a specific field)
        if 'field_name' in context:
            # We're validating a specific field
            field_index = self.source_fields.index(context['field_name'])
            if field_index >= 0:
                # Just check this specific value
                return resolver.exists(self.target_table, self.target_fields[field_index], value)
        
        # We're validating the entire relationship
        return resolver.exists_composite(self.target_table, self.target_fields, source_values)
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a foreign key constraint violation"""
        field_values = context.get('field_values', {})
        
        if 'field_name' in context:
            field_name = context['field_name']
            field_index = self.source_fields.index(field_name) if field_name in self.source_fields else -1
            
            if field_index >= 0:
                target_field = self.target_fields[field_index]
                return f"Value '{value}' in field '{field_name}' does not reference a valid '{target_field}' in table '{self.target_table}'"
        
        # For composite keys or general case
        source_values = [field_values.get(field) for field in self.source_fields]
        return f"Values {source_values} do not reference valid keys {self.target_fields} in table '{self.target_table}'"


class UniqueKeyConstraint(RelationshipConstraint):
    """Constraint for unique keys within a table"""
    fields: List[str]  # Fields that form the unique key
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate that a key is unique within a table
        
        Note: This requires:
        - 'existing_keys' in the context with all existing keys
        - 'field_values' dict with values for all key fields
        """
        existing_keys = context.get('existing_keys', [])
        field_values = context.get('field_values', {})
        
        # Extract values for all key fields
        key_values = tuple(field_values.get(field) for field in self.fields)
        
        # Check if this key already exists
        return key_values not in existing_keys
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a unique key constraint violation"""
        field_values = context.get('field_values', {})
        key_values = tuple(field_values.get(field) for field in self.fields)
        return f"Key {key_values} for fields {self.fields} is not unique"


class PrimaryKeyConstraint(UniqueKeyConstraint):
    """Constraint for primary keys"""
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate that a primary key is valid
        
        Note: This extends UniqueKeyConstraint with additional checks:
        - None of the key fields can be NULL
        """
        field_values = context.get('field_values', {})
        
        # Check that none of the key fields are NULL
        for field in self.fields:
            if field_values.get(field) is None:
                return False
        
        # Delegate to parent for uniqueness check
        return super().validate(value, context)
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a primary key constraint violation"""
        field_values = context.get('field_values', {})
        
        # Check for NULL values first
        for field in self.fields:
            if field_values.get(field) is None:
                return f"Primary key field '{field}' cannot be NULL"
        
        # If not NULL, it's a uniqueness violation
        return f"Primary key {tuple(field_values.get(field) for field in self.fields)} is not unique"


class CheckConstraint(RelationshipConstraint):
    """Constraint for table-level check constraints"""
    expression: str  # Expression in the DSL syntax
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate that a table satisfies a check constraint
        
        Note: This requires:
        - An expression evaluator in the context
        - A 'field_values' dict with values for all fields referenced in the expression
        """
        evaluator = context.get('expression_evaluator')
        if not evaluator:
            raise ValueError("Expression evaluator not provided in context")
            
        field_values = context.get('field_values', {})
        
        # Combine the field values and context for expression evaluation
        eval_context = {**field_values, **context}
        
        try:
            return evaluator.evaluate(self.expression, eval_context)
        except Exception as e:
            # Log the error and fail the constraint
            print(f"Error evaluating expression '{self.expression}': {e}")
            return False
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a check constraint violation"""
        return f"Table check constraint '{self.expression}' is not satisfied"



