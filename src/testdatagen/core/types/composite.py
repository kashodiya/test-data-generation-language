

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

from .primitive import TypeBase, TypeCategory, PrimitiveType


class CompositeTypeKind(str, Enum):
    """Kinds of composite types supported by the DSL"""
    ARRAY = "array"
    OBJECT = "object"
    ENUM = "enum"


class CompositeType(TypeBase):
    """Definition of a composite type"""
    category: TypeCategory = TypeCategory.COMPOSITE
    kind: CompositeTypeKind


class ArrayType(CompositeType):
    """Definition of an array type"""
    kind: CompositeTypeKind = CompositeTypeKind.ARRAY
    item_type: Union[TypeBase, str]  # Can be a type instance or a reference to a type by name
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    unique_items: bool = False
    
    @classmethod
    def create(cls, item_type: Union[TypeBase, str], nullable: bool = True,
               min_items: Optional[int] = None, max_items: Optional[int] = None,
               unique_items: bool = False, description: Optional[str] = None) -> 'ArrayType':
        """Create an array type"""
        type_name = f"array<{item_type if isinstance(item_type, str) else item_type.name}>"
        return cls(
            name=type_name,
            item_type=item_type,
            nullable=nullable,
            min_items=min_items,
            max_items=max_items,
            unique_items=unique_items,
            description=description
        )


class ObjectField(BaseModel):
    """Definition of a field in an object type"""
    name: str
    type: Union[TypeBase, str]  # Can be a type instance or a reference to a type by name
    required: bool = True
    description: Optional[str] = None


class ObjectType(CompositeType):
    """Definition of an object type"""
    kind: CompositeTypeKind = CompositeTypeKind.OBJECT
    fields: List[ObjectField]
    additional_properties: bool = False
    
    @classmethod
    def create(cls, name: str, fields: List[ObjectField], nullable: bool = True,
               additional_properties: bool = False, description: Optional[str] = None) -> 'ObjectType':
        """Create an object type"""
        return cls(
            name=name,
            fields=fields,
            nullable=nullable,
            additional_properties=additional_properties,
            description=description
        )


class EnumValue(BaseModel):
    """Definition of a value in an enum type"""
    name: str
    value: Any
    description: Optional[str] = None


class EnumType(CompositeType):
    """Definition of an enum type"""
    kind: CompositeTypeKind = CompositeTypeKind.ENUM
    values: List[EnumValue]
    
    @classmethod
    def create(cls, name: str, values: List[EnumValue], nullable: bool = True,
               description: Optional[str] = None) -> 'EnumType':
        """Create an enum type"""
        return cls(
            name=name,
            values=values,
            nullable=nullable,
            description=description
        )

