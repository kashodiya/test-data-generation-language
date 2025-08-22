
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class TypeCategory(str, Enum):
    """Categories of data types in the DSL"""
    PRIMITIVE = "primitive"
    COMPOSITE = "composite"
    CUSTOM = "custom"


class PrimitiveTypeKind(str, Enum):
    """Kinds of primitive types supported by the DSL"""
    INTEGER = "integer"
    DECIMAL = "decimal"
    STRING = "string"
    BOOLEAN = "boolean"
    DATE = "date"
    TIMESTAMP = "timestamp"
    BINARY = "binary"
    UUID = "uuid"
    JSON = "json"


class TypeBase(BaseModel):
    """Base class for all type definitions"""
    name: str
    category: TypeCategory
    nullable: bool = True
    description: Optional[str] = None


class PrimitiveType(TypeBase):
    """Definition of a primitive type"""
    category: TypeCategory = TypeCategory.PRIMITIVE
    kind: PrimitiveTypeKind
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    pattern: Optional[str] = None
    format: Optional[str] = None
    
    @classmethod
    def integer(cls, nullable: bool = True, min_value: Optional[int] = None, 
                max_value: Optional[int] = None, description: Optional[str] = None) -> 'PrimitiveType':
        """Create an integer type"""
        return cls(
            name="integer",
            kind=PrimitiveTypeKind.INTEGER,
            nullable=nullable,
            min_value=min_value,
            max_value=max_value,
            description=description
        )
    
    @classmethod
    def decimal(cls, nullable: bool = True, min_value: Optional[float] = None,
                max_value: Optional[float] = None, description: Optional[str] = None) -> 'PrimitiveType':
        """Create a decimal type"""
        return cls(
            name="decimal",
            kind=PrimitiveTypeKind.DECIMAL,
            nullable=nullable,
            min_value=min_value,
            max_value=max_value,
            description=description
        )
    
    @classmethod
    def string(cls, nullable: bool = True, pattern: Optional[str] = None,
               format: Optional[str] = None, description: Optional[str] = None) -> 'PrimitiveType':
        """Create a string type"""
        return cls(
            name="string",
            kind=PrimitiveTypeKind.STRING,
            nullable=nullable,
            pattern=pattern,
            format=format,
            description=description
        )
    
    @classmethod
    def boolean(cls, nullable: bool = True, description: Optional[str] = None) -> 'PrimitiveType':
        """Create a boolean type"""
        return cls(
            name="boolean",
            kind=PrimitiveTypeKind.BOOLEAN,
            nullable=nullable,
            description=description
        )
    
    @classmethod
    def date(cls, nullable: bool = True, min_value: Optional[str] = None,
             max_value: Optional[str] = None, format: Optional[str] = None,
             description: Optional[str] = None) -> 'PrimitiveType':
        """Create a date type"""
        return cls(
            name="date",
            kind=PrimitiveTypeKind.DATE,
            nullable=nullable,
            min_value=min_value,
            max_value=max_value,
            format=format,
            description=description
        )
    
    @classmethod
    def timestamp(cls, nullable: bool = True, min_value: Optional[str] = None,
                  max_value: Optional[str] = None, format: Optional[str] = None,
                  description: Optional[str] = None) -> 'PrimitiveType':
        """Create a timestamp type"""
        return cls(
            name="timestamp",
            kind=PrimitiveTypeKind.TIMESTAMP,
            nullable=nullable,
            min_value=min_value,
            max_value=max_value,
            format=format,
            description=description
        )
    
    @classmethod
    def binary(cls, nullable: bool = True, description: Optional[str] = None) -> 'PrimitiveType':
        """Create a binary type"""
        return cls(
            name="binary",
            kind=PrimitiveTypeKind.BINARY,
            nullable=nullable,
            description=description
        )
    
    @classmethod
    def uuid(cls, nullable: bool = True, description: Optional[str] = None) -> 'PrimitiveType':
        """Create a UUID type"""
        return cls(
            name="uuid",
            kind=PrimitiveTypeKind.UUID,
            nullable=nullable,
            description=description
        )
    
    @classmethod
    def json(cls, nullable: bool = True, description: Optional[str] = None) -> 'PrimitiveType':
        """Create a JSON type"""
        return cls(
            name="json",
            kind=PrimitiveTypeKind.JSON,
            nullable=nullable,
            description=description
        )
