



from typing import Any, Dict, List, Optional, Union, Callable
from pydantic import BaseModel, Field

from .base import Constraint, ConstraintType


class BusinessRuleConstraint(Constraint):
    """Base class for business rule constraints"""
    constraint_type: ConstraintType = ConstraintType.BUSINESS


class ExpressionConstraint(BusinessRuleConstraint):
    """Constraint based on a boolean expression"""
    expression: str  # Expression in the DSL syntax
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate that a value satisfies the expression
        
        Note: This requires an expression evaluator in the context
        """
        evaluator = context.get('expression_evaluator')
        if not evaluator:
            raise ValueError("Expression evaluator not provided in context")
            
        # Combine the value and context for expression evaluation
        eval_context = {'value': value, **context}
        
        try:
            return evaluator.evaluate(self.expression, eval_context)
        except Exception as e:
            # Log the error and fail the constraint
            print(f"Error evaluating expression '{self.expression}': {e}")
            return False
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for an expression constraint violation"""
        return f"Value '{value}' does not satisfy expression '{self.expression}'"


class ConditionalConstraint(BusinessRuleConstraint):
    """Constraint that applies only when a condition is met"""
    condition: str  # Condition expression in the DSL syntax
    then_constraint: Constraint  # Constraint to apply when condition is true
    else_constraint: Optional[Constraint] = None  # Optional constraint to apply when condition is false
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate based on a condition
        
        Note: This requires an expression evaluator in the context
        """
        evaluator = context.get('expression_evaluator')
        if not evaluator:
            raise ValueError("Expression evaluator not provided in context")
            
        # Combine the value and context for expression evaluation
        eval_context = {'value': value, **context}
        
        try:
            condition_result = evaluator.evaluate(self.condition, eval_context)
            
            if condition_result:
                return self.then_constraint.validate(value, context)
            elif self.else_constraint:
                return self.else_constraint.validate(value, context)
            else:
                # If no else constraint and condition is false, the constraint is satisfied
                return True
        except Exception as e:
            # Log the error and fail the constraint
            print(f"Error evaluating condition '{self.condition}': {e}")
            return False
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a conditional constraint violation"""
        evaluator = context.get('expression_evaluator')
        if not evaluator:
            return super().get_error_message(value, context)
            
        eval_context = {'value': value, **context}
        
        try:
            condition_result = evaluator.evaluate(self.condition, eval_context)
            
            if condition_result:
                return self.then_constraint.get_error_message(value, context)
            elif self.else_constraint:
                return self.else_constraint.get_error_message(value, context)
            else:
                return super().get_error_message(value, context)
        except Exception:
            return f"Error evaluating condition '{self.condition}' for value '{value}'"


class CustomConstraint(BusinessRuleConstraint):
    """Constraint based on a custom validation function"""
    validator_name: str  # Name of the validator function
    parameters: Dict[str, Any] = Field(default_factory=dict)  # Parameters for the validator
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate using a custom validator function
        
        Note: This requires a validator registry in the context
        """
        validator_registry = context.get('validator_registry')
        if not validator_registry:
            raise ValueError("Validator registry not provided in context")
            
        validator = validator_registry.get(self.validator_name)
        if not validator:
            raise ValueError(f"Validator '{self.validator_name}' not found in registry")
            
        try:
            return validator(value, self.parameters, context)
        except Exception as e:
            # Log the error and fail the constraint
            print(f"Error in custom validator '{self.validator_name}': {e}")
            return False
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a custom constraint violation"""
        return f"Value '{value}' does not satisfy custom constraint '{self.validator_name}'"


class DependentFieldConstraint(BusinessRuleConstraint):
    """Constraint that depends on other field values"""
    field_dependencies: List[str]  # List of field names this constraint depends on
    expression: str  # Expression in the DSL syntax that references other fields
    
    def validate(self, value: Any, context: Dict[str, Any]) -> bool:
        """
        Validate based on dependencies between fields
        
        Note: This requires:
        - An expression evaluator in the context
        - A 'field_values' dict in the context with values for all dependent fields
        """
        evaluator = context.get('expression_evaluator')
        if not evaluator:
            raise ValueError("Expression evaluator not provided in context")
            
        field_values = context.get('field_values', {})
        
        # Check that all dependencies are present
        for field in self.field_dependencies:
            if field not in field_values:
                raise ValueError(f"Dependent field '{field}' not found in context")
        
        # Combine the value, field values, and context for expression evaluation
        eval_context = {'value': value, **field_values, **context}
        
        try:
            return evaluator.evaluate(self.expression, eval_context)
        except Exception as e:
            # Log the error and fail the constraint
            print(f"Error evaluating expression '{self.expression}': {e}")
            return False
    
    def get_error_message(self, value: Any, context: Dict[str, Any]) -> str:
        """Get an error message for a dependent field constraint violation"""
        field_values = context.get('field_values', {})
        dependencies = {field: field_values.get(field, 'N/A') for field in self.field_dependencies}
        return f"Value '{value}' with dependencies {dependencies} does not satisfy expression '{self.expression}'"



