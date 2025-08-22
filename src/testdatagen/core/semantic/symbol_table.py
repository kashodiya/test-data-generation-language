




from typing import Dict, List, Optional, Any, Set
from pydantic import BaseModel


class Symbol(BaseModel):
    """Represents a symbol in the symbol table"""
    name: str
    kind: str  # 'schema', 'table', 'field', 'type', 'constraint', etc.
    type: Optional[str] = None
    attributes: Dict[str, Any] = {}
    source_line: int = 0
    source_column: int = 0


class Scope(BaseModel):
    """Represents a scope in the symbol table"""
    name: str
    parent: Optional['Scope'] = None
    symbols: Dict[str, Symbol] = {}
    children: Dict[str, 'Scope'] = {}
    
    def add_symbol(self, symbol: Symbol) -> None:
        """Add a symbol to this scope"""
        self.symbols[symbol.name] = symbol
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in this scope"""
        return self.symbols.get(name)
    
    def lookup_recursive(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in this scope and parent scopes"""
        symbol = self.lookup(name)
        if symbol is not None:
            return symbol
        
        if self.parent is not None:
            return self.parent.lookup_recursive(name)
        
        return None
    
    def add_child_scope(self, name: str) -> 'Scope':
        """Add a child scope to this scope"""
        child = Scope(name=name, parent=self)
        self.children[name] = child
        return child
    
    def get_child_scope(self, name: str) -> Optional['Scope']:
        """Get a child scope by name"""
        return self.children.get(name)
    
    def get_all_symbols(self) -> List[Symbol]:
        """Get all symbols in this scope"""
        return list(self.symbols.values())
    
    def get_symbols_by_kind(self, kind: str) -> List[Symbol]:
        """Get all symbols of a specific kind in this scope"""
        return [s for s in self.symbols.values() if s.kind == kind]


class SymbolTable:
    """Symbol table for semantic analysis"""
    
    def __init__(self):
        self.global_scope = Scope(name="global")
        self.current_scope = self.global_scope
        
    def enter_scope(self, name: str) -> None:
        """Enter a new scope"""
        scope = self.current_scope.get_child_scope(name)
        if scope is None:
            scope = self.current_scope.add_child_scope(name)
        self.current_scope = scope
        
    def exit_scope(self) -> None:
        """Exit the current scope"""
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent
            
    def add_symbol(self, symbol: Symbol) -> None:
        """Add a symbol to the current scope"""
        self.current_scope.add_symbol(symbol)
        
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in the current scope"""
        return self.current_scope.lookup(name)
        
    def lookup_recursive(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in the current scope and parent scopes"""
        return self.current_scope.lookup_recursive(name)
    
    def get_current_scope(self) -> Scope:
        """Get the current scope"""
        return self.current_scope
    
    def get_global_scope(self) -> Scope:
        """Get the global scope"""
        return self.global_scope
    
    def get_all_symbols(self) -> List[Symbol]:
        """Get all symbols in the current scope"""
        return self.current_scope.get_all_symbols()
    
    def get_symbols_by_kind(self, kind: str) -> List[Symbol]:
        """Get all symbols of a specific kind in the current scope"""
        return self.current_scope.get_symbols_by_kind(kind)




