













from typing import List, Tuple, Union
from antlr4 import InputStream, FileStream
from pydantic import BaseModel

from ..ast.nodes import SchemaNode
from .builder import ASTBuilder
from .error_listener import TestDataGenErrorListener, SyntaxError


class ParseResult(BaseModel):
    """Result of parsing a DSL file"""
    ast: Union[SchemaNode, None]
    errors: List[SyntaxError]
    success: bool


class Parser:
    """Parser for the TestDataGen DSL"""
    
    def __init__(self):
        self.builder = ASTBuilder()
        self.error_listener = TestDataGenErrorListener()
    
    def parse_string(self, input_string: str) -> ParseResult:
        """Parse a DSL string"""
        input_stream = InputStream(input_string)
        return self._parse(input_stream)
    
    def parse_file(self, file_path: str) -> ParseResult:
        """Parse a DSL file"""
        input_stream = FileStream(file_path)
        return self._parse(input_stream)
    
    def _parse(self, input_stream: InputStream) -> ParseResult:
        """Parse an input stream"""
        # Reset error listener
        self.error_listener = TestDataGenErrorListener()
        
        try:
            # Build AST
            ast = self.builder.build(input_stream)
            
            # Check for syntax errors
            if self.error_listener.has_errors():
                return ParseResult(
                    ast=None,
                    errors=self.error_listener.get_errors(),
                    success=False
                )
            
            return ParseResult(
                ast=ast,
                errors=[],
                success=True
            )
        except Exception as e:
            # Handle unexpected errors
            error = SyntaxError(
                message=f"Unexpected error: {str(e)}",
                line=0,
                column=0
            )
            return ParseResult(
                ast=None,
                errors=[error],
                success=False
            )
