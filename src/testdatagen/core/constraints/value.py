



from typing import Any, Dict, List, Optional, Union, Pattern
import re
from datetime import datetime
from pydantic import BaseModel, Field

from .base import Constraint, ConstraintType


class ValueConstraint(Constraint):
    """Base class for value constraints"""
    constraint_type: ConstraintType = ConstraintType.VALUE


class RangeConstraint(ValueConstraint):
    """Constraint for numeric ranges"""
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    inclusive_min: bool = True
    inclusive_max: bool = True
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """Validate that a value is within the specified range"""
        if value is None:
            return True
            
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            return False
            
        if self.min_value is not None:
            if self.inclusive_min:
                if numeric_value < self.min_value:
                    return False
            else:
                if numeric_value <= self.min_value:
                    return False
                    
        if self.max_value is not None:
            if self.inclusive_max:
                if numeric_value > self.max_value:
                    return False
            else:
                if numeric_value >= self.max_value:
                    return False
                    
        return True
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a range constraint violation"""
        min_op = ">=" if self.inclusive_min else ">"
        max_op = "<=" if self.inclusive_max else "<"
        
        if self.min_value is not None and self.max_value is not None:
            return f"Value {value} must be {min_op} {self.min_value} and {max_op} {self.max_value}"
        elif self.min_value is not None:
            return f"Value {value} must be {min_op} {self.min_value}"
        elif self.max_value is not None:
            return f"Value {value} must be {max_op} {self.max_value}"
        else:
            return super().get_error_message(value, context)


class LengthConstraint(ValueConstraint):
    """Constraint for string length"""
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """Validate that a string's length is within the specified range"""
        if value is None:
            return True
            
        try:
            length = len(str(value))
        except (ValueError, TypeError):
            return False
            
        if self.min_length is not None and length < self.min_length:
            return False
            
        if self.max_length is not None and length > self.max_length:
            return False
            
        return True
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a length constraint violation"""
        if self.min_length is not None and self.max_length is not None:
            return f"Length of '{value}' must be between {self.min_length} and {self.max_length}"
        elif self.min_length is not None:
            return f"Length of '{value}' must be at least {self.min_length}"
        elif self.max_length is not None:
            return f"Length of '{value}' must be at most {self.max_length}"
        else:
            return super().get_error_message(value, context)


class PatternConstraint(ValueConstraint):
    """Constraint for string patterns"""
    pattern: str
    _compiled_pattern: Optional[Pattern] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self._compiled_pattern = re.compile(self.pattern)
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """Validate that a string matches the specified pattern"""
        if value is None:
            return True
            
        try:
            return bool(self._compiled_pattern.match(str(value)))
        except (ValueError, TypeError):
            return False
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a pattern constraint violation"""
        return f"Value '{value}' does not match pattern '{self.pattern}'"


class EnumConstraint(ValueConstraint):
    """Constraint for enumerated values"""
    allowed_values: List[Any]
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """Validate that a value is one of the allowed values"""
        if value is None:
            return True
            
        return value in self.allowed_values
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for an enum constraint violation"""
        return f"Value '{value}' is not one of the allowed values: {', '.join(map(str, self.allowed_values))}"


class DateRangeConstraint(ValueConstraint):
    """Constraint for date ranges"""
    min_date: Optional[str] = None
    max_date: Optional[str] = None
    date_format: str = "%Y-%m-%d"
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """Validate that a date is within the specified range"""
        if value is None:
            return True
            
        try:
            if isinstance(value, str):
                date_value = datetime.strptime(value, self.date_format)
            elif isinstance(value, datetime):
                date_value = value
            else:
                return False
                
            if self.min_date is not None:
                min_date = datetime.strptime(self.min_date, self.date_format)
                if date_value < min_date:
                    return False
                    
            if self.max_date is not None:
                max_date = datetime.strptime(self.max_date, self.date_format)
                if date_value > max_date:
                    return False
                    
            return True
        except (ValueError, TypeError):
            return False
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a date range constraint violation"""
        if self.min_date is not None and self.max_date is not None:
            return f"Date '{value}' must be between {self.min_date} and {self.max_date}"
        elif self.min_date is not None:
            return f"Date '{value}' must be on or after {self.min_date}"
        elif self.max_date is not None:
            return f"Date '{value}' must be on or before {self.max_date}"
        else:
            return super().get_error_message(value, context)


class UniqueConstraint(ValueConstraint):
    """Constraint for unique values"""
    scope: Optional[List[str]] = None  # List of field names that form a composite unique constraint
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate that a value is unique within its scope
        
        Note: This constraint requires context to contain:
        - 'existing_values': List of existing values
        - 'field_values': Dict of field values for composite constraints
        """
        if value is None:
            return True
            
        existing_values = context.get('existing_values', [])
        
        if self.scope:
            # For composite unique constraints
            field_values = context.get('field_values', {})
            
            # Create a tuple of values for the composite key
            composite_key = tuple(field_values.get(field, None) for field in self.scope)
            
            # Check if this composite key already exists
            return composite_key not in existing_values
        else:
            # For simple unique constraints
            return value not in existing_values
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a unique constraint violation"""
        if self.scope:
            field_values = context.get('field_values', {})
            composite_key = tuple(field_values.get(field, None) for field in self.scope)
            return f"Composite key {composite_key} for fields {self.scope} is not unique"
        else:
            return f"Value '{value}' is not unique"


class NotNullConstraint(ValueConstraint):
    """Constraint for non-null values"""
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """Validate that a value is not null"""
        return value is not None
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a not-null constraint violation"""
        return "Value cannot be null"


