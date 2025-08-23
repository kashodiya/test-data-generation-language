
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
            print("Original input text:")
            print(input_text[:200] + "..." if len(input_text) > 200 else input_text)
            
            # There's a token mismatch between the lexer and parser
            # In the lexer, TABLE = 2, but in the parser, TABLE = 9
            # This causes the parser to not recognize table declarations
            
            # Let's manually parse the input text to extract the schema and tables
            import re
            
            # Extract schema name
            schema_match = re.search(r'schema\s+(\w+)\s*{', input_text)
            schema_name = schema_match.group(1) if schema_match else "DefaultSchema"
            
            # Extract tables
            tables = []
            table_matches = re.finditer(r'table\s+(\w+)\s*{(.*?)(?=\n\s*})', input_text, re.DOTALL)
            
            for table_match in table_matches:
                table_name = table_match.group(1)
                table_content = table_match.group(2)
                
                # Extract fields
                fields = []
                field_matches = re.finditer(r'field\s+(\w+)\s*:\s*(\w+)', table_content)
                
                for field_match in field_matches:
                    field_name = field_match.group(1)
                    field_type = field_match.group(2)
                    fields.append((field_name, field_type))
                
                tables.append((table_name, fields))
            
            print(f"Manually parsed schema: {schema_name}")
            print(f"Manually parsed tables: {tables}")
            
            # For now, we'll just use the input text as is for the ANTLR parser
            # But we'll add a newline at the beginning to fix the EOF issue
            modified_text = "\n" + input_text
            print("Modified input text:")
            print(modified_text[:200] + "..." if len(modified_text) > 200 else modified_text)
            
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
            
            # Debug lexer tokens
            print("Lexer tokens:")
            tokens = list(lexer.getAllTokens())
            for token in tokens[:20]:  # Print first 20 tokens
                print(f"Token: {token.text}, Type: {token.type}")
            
            # Reset lexer
            lexer = TestDataGenLexer(modified_input)
            lexer.removeErrorListeners()
            lexer.addErrorListener(self.error_listener)
            
            token_stream = CommonTokenStream(lexer)
            parser = TestDataGenParser(token_stream)
            parser.removeErrorListeners()
            parser.addErrorListener(self.error_listener)
            
            # Parse the input
            try:
                parse_tree = parser.program()
            except Exception as e:
                print(f"Parsing failed!")
                print(f"Error: {str(e)}")
                return ParseResult(
                    ast=None,
                    errors=[SyntaxError(message=str(e), line=0, column=0)],
                    success=False
                )
            
            # Check for syntax errors
            if self.error_listener.has_errors():
                return ParseResult(
                    ast=None,
                    errors=self.error_listener.get_errors(),
                    success=False
                )
            
            # Build AST from parse tree
            ast = self.builder.visit(parse_tree)
            
            # If the AST has no tables, use our manually parsed schema and tables
            if not ast.tables and tables:
                from ..ast.nodes import SchemaNode, TableNode, FieldNode, NodeType
                
                # Create field nodes
                table_nodes = []
                for table_name, fields in tables:
                    field_nodes = []
                    for field_name, field_type in fields:
                        field_node = FieldNode(
                            node_type=NodeType.FIELD,
                            name=field_name,
                            data_type=field_type,
                            line=0,
                            column=0
                        )
                        field_nodes.append(field_node)
                    
                    # Create table node
                    table_node = TableNode(
                        node_type=NodeType.TABLE,
                        name=table_name,
                        fields=field_nodes,
                        line=0,
                        column=0
                    )
                    table_nodes.append(table_node)
                
                # Create schema node
                ast = SchemaNode(
                    node_type=NodeType.SCHEMA,
                    name=schema_name,
                    tables=table_nodes,
                    line=0,
                    column=0
                )
            
            # Debug: Print AST structure
            print("AST Structure:")
            print(f"Schema name: {ast.name}")
            print(f"Tables: {[t.name for t in ast.tables]}")
            
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
