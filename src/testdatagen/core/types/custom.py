

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

from .primitive import TypeBase, TypeCategory


class CustomType(TypeBase):
    """Definition of a custom type"""
    category: TypeCategory = TypeCategory.CUSTOM
    base_type: Union[TypeBase, str]  # Can be a type instance or a reference to a type by name
    validators: List[str] = Field(default_factory=list)  # List of validator function names
    constraints: List[Dict[str, Any]] = Field(default_factory=list)  # List of constraints
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @classmethod
    def create(cls, name: str, base_type: Union[TypeBase, str], nullable: bool = True,
               validators: Optional[List[str]] = None, constraints: Optional[List[Dict[str, Any]]] = None,
               metadata: Optional[Dict[str, Any]] = None, description: Optional[str] = None) -> 'CustomType':
        """Create a custom type"""
        return cls(
            name=name,
            base_type=base_type,
            nullable=nullable,
            validators=validators or [],
            constraints=constraints or [],
            metadata=metadata or {},
            description=description
        )
        
    def add_constraint(self, constraint_type: str, parameters: Dict[str, Any]) -> None:
        """Add a constraint to the custom type"""
        self.constraints.append({
            "type": constraint_type,
            "parameters": parameters
        })
        
    def get_constraints(self) -> List[Dict[str, Any]]:
        """Get all constraints for this custom type"""
        return self.constraints

