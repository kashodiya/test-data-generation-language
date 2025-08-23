


from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel

from .primitive import TypeBase, PrimitiveType, PrimitiveTypeKind, TypeCategory
from .composite import CompositeType, ArrayType, ObjectType, EnumType, CompositeTypeKind
from .custom import CustomType


class TypeRegistry:
    """Registry for all types in the system"""
    
    def __init__(self):
        self._types: Dict[str, TypeBase] = {}
        self._initialize_primitive_types()
    
    def _initialize_primitive_types(self):
        """Initialize the registry with primitive types"""
        self.register(PrimitiveType.integer())
        self.register(PrimitiveType.decimal())
        self.register(PrimitiveType.string())
        self.register(PrimitiveType.boolean())
        self.register(PrimitiveType.date())
        self.register(PrimitiveType.timestamp())
        self.register(PrimitiveType.binary())
        self.register(PrimitiveType.uuid())
        self.register(PrimitiveType.json())
        
        # Register enum as a special type
        from .composite import EnumType, EnumValue
        self.register(EnumType(
            name="enum",
            values=[],
            category=TypeCategory.COMPOSITE,
            kind=CompositeTypeKind.ENUM
        ))
    
    def register(self, type_def: TypeBase) -> None:
        """Register a type in the registry"""
        if type_def.name in self._types:
            raise ValueError(f"Type '{type_def.name}' is already registered")
        self._types[type_def.name] = type_def
    
    def get(self, name: str) -> Optional[TypeBase]:
        """Get a type by name"""
        return self._types.get(name)
    
    def exists(self, name: str) -> bool:
        """Check if a type exists in the registry"""
        return name in self._types
    
    def list_types(self, category: Optional[TypeCategory] = None) -> List[TypeBase]:
        """List all types in the registry, optionally filtered by category"""
        if category is None:
            return list(self._types.values())
        return [t for t in self._types.values() if t.category == category]
    
    def create_array_type(self, item_type: Union[TypeBase, str], **kwargs) -> ArrayType:
        """Create and register an array type"""
        array_type = ArrayType.create(item_type, **kwargs)
        self.register(array_type)
        return array_type
    
    def create_object_type(self, name: str, fields: List[Any], **kwargs) -> ObjectType:
        """Create and register an object type"""
        object_type = ObjectType.create(name, fields, **kwargs)
        self.register(object_type)
        return object_type
    
    def create_enum_type(self, name: str, values: List[Any], **kwargs) -> EnumType:
        """Create and register an enum type"""
        enum_type = EnumType.create(name, values, **kwargs)
        self.register(enum_type)
        return enum_type
    
    def create_custom_type(self, name: str, base_type: Union[TypeBase, str], constraints: Optional[List[Dict[str, Any]]] = None, **kwargs) -> CustomType:
        """Create and register a custom type"""
        custom_type = CustomType.create(name, base_type, constraints=constraints, **kwargs)
        self.register(custom_type)
        return custom_type
        
    def register_custom_type_from_ast(self, type_node) -> CustomType:
        """Register a custom type from an AST node"""
        # Extract constraints from the AST node
        constraints = []
        for constraint in type_node.constraints:
            constraints.append({
                "type": constraint.constraint_type,
                "parameters": constraint.parameters
            })
            
        # Create and register the custom type
        return self.create_custom_type(
            name=type_node.name,
            base_type=type_node.base_type,
            constraints=constraints,
            description=f"Custom type defined in schema"
        )
    
    def resolve_type_reference(self, type_ref: Union[TypeBase, str]) -> Optional[TypeBase]:
        """Resolve a type reference to a concrete type"""
        if isinstance(type_ref, TypeBase):
            return type_ref
        return self.get(type_ref)


# Global type registry instance
default_registry = TypeRegistry()

