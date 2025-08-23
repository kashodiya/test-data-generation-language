
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class NodeType(str, Enum):
    SCHEMA = "schema"
    TABLE = "table"
    FIELD = "field"
    CONSTRAINT = "constraint"
    TYPE = "type"


class ASTNode(BaseModel):
    """Base class for all AST nodes"""
    node_type: NodeType
    line: int = Field(description="Line number in source")
    column: int = Field(description="Column number in source")


class ConstraintNode(ASTNode):
    """Base class for all constraint nodes"""
    name: str
    constraint_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class FieldNode(ASTNode):
    """Field definition within a table"""
    name: str
    data_type: str
    constraints: List[ConstraintNode] = Field(default_factory=list)
    nullable: bool = True
    default_value: Optional[Any] = None


class TableNode(ASTNode):
    """Table definition within a schema"""
    name: str
    fields: List[FieldNode]
    constraints: List[ConstraintNode] = Field(default_factory=list)


class TypeNode(ASTNode):
    """Type definition within a schema"""
    name: str
    base_type: str
    constraints: List[ConstraintNode] = Field(default_factory=list)


class SchemaNode(ASTNode):
    """Root node for a schema definition"""
    name: str
    types: List[TypeNode] = Field(default_factory=list)
    tables: List[TableNode]
    imports: List[str] = Field(default_factory=list)
