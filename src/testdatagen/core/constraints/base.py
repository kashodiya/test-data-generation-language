


from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ConstraintType(str, Enum):
    """Types of constraints supported by the DSL"""
    VALUE = "value"           # Constraints on field values
    BUSINESS = "business"     # Business rule constraints
    RELATIONSHIP = "relationship"  # Constraints on relationships between tables


class ConstraintSeverity(str, Enum):
    """Severity levels for constraint violations"""
    ERROR = "error"           # Hard constraint, must be satisfied
    WARNING = "warning"       # Soft constraint, violation generates warning
    INFO = "info"             # Informational constraint, violation is logged


class Constraint(BaseModel):
    """Base class for all constraints"""
    name: str
    constraint_type: ConstraintType
    description: Optional[str] = None
    severity: ConstraintSeverity = ConstraintSeverity.ERROR
    enabled: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate the constraint against a value
        
        Args:
            value: The value to validate
            context: Additional context for validation
            
        Returns:
            True if the constraint is satisfied, False otherwise
        """
        raise NotImplementedError("Subclasses must implement validate()")
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """
        Get an error message for a constraint violation
        
        Args:
            value: The value that violated the constraint
            context: Additional context for the error message
            
        Returns:
            An error message describing the violation
        """
        return f"Constraint '{self.name}' violated"


class ConstraintViolation(BaseModel):
    """Represents a constraint violation"""
    constraint: Constraint
    value: Any
    context: Dict[str, Any]
    message: str
    
    @classmethod
    def create(cls, constraint: Constraint, value: Any, context: Dict[str, Any]) -> 'ConstraintViolation':
        """Create a constraint violation"""
        return cls(
            constraint=constraint,
            value=value,
            context=context,
            message=constraint.get_error_message(value, context)
        )


class ConstraintValidator:
    """Validates constraints against values"""
    
    def validate(self, value: Any, constraints: List[Constraint], context: Dict[str, Any]) -> List[ConstraintViolation]:
        """
        Validate constraints against a value
        
        Args:
            value: The value to validate
            constraints: The constraints to validate
            context: Additional context for validation
            
        Returns:
            A list of constraint violations, empty if all constraints are satisfied
        """
        violations = []
        
        for constraint in constraints:
            if not constraint.enabled:
                continue
                
            if not constraint.validate(value, context):
                violations.append(ConstraintViolation.create(constraint, value, context))
        
        return violations


