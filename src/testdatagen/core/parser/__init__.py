













from typing import List, Tuple, Union
from antlr4 import InputStream, FileStream
from pydantic import BaseModel

from ..ast.nodes import SchemaNode
from .builder import ASTBuilder
from .error_listener import TestDataGenErrorListener, SyntaxError
from .custom_error_listener import CustomErrorListener


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
        self.error_listener = CustomErrorListener()
        
        try:
            # Preprocess the input to fix schema name format
            import re
            input_text = input_stream.strdata
            modified_text = re.sub(r'schema\s+(\w+)\s+{', r'schema "\1" {', input_text)
            
            # Create a new input stream with the modified text
            from antlr4 import InputStream as ANTLRInputStream
            modified_input = ANTLRInputStream(modified_text)
            
            # Build AST
            from antlr4 import CommonTokenStream
            from .generated.TestDataGenLexer import TestDataGenLexer
            from .generated.TestDataGenParser import TestDataGenParser
            
            # Create lexer and parser
            lexer = TestDataGenLexer(modified_input)
            lexer.removeErrorListeners()
            lexer.addErrorListener(self.error_listener)
            
            token_stream = CommonTokenStream(lexer)
            parser = TestDataGenParser(token_stream)
            parser.removeErrorListeners()
            parser.addErrorListener(self.error_listener)
            
            # Parse the input
            parse_tree = parser.program()
            
            # Check for syntax errors
            if self.error_listener.has_errors():
                return ParseResult(
                    ast=None,
                    errors=self.error_listener.get_errors(),
                    success=False
                )
            
            # Build AST from parse tree
            ast = self.builder.visit(parse_tree)
            
            return ParseResult(
                ast=ast,
                errors=[],
                success=True
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
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
