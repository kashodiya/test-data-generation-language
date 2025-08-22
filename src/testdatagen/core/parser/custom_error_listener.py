
from typing import List
from antlr4.error.ErrorListener import ErrorListener
from pydantic import BaseModel
from .error_listener import SyntaxError


class CustomErrorListener(ErrorListener):
    """Custom error listener for ANTLR that ignores schema name format errors"""
    
    def __init__(self):
        super().__init__()
        self.errors: List[SyntaxError] = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """Called when a syntax error occurs"""
        # Add more detailed information to the error message
        detailed_msg = msg
        if offendingSymbol:
            detailed_msg += f" (Symbol: {offendingSymbol.text}, Type: {offendingSymbol.type})"
        
        # Special case: ignore the specific error about schema name
        if offendingSymbol and "expecting STRING_LITERAL" in msg:
            # This is the error we want to ignore
            # We'll handle it in the parser
            print(f"Ignoring schema name format error at line {line}:{column}")
            return
        
        # Print detailed error for debugging
        print(f"Syntax error at line {line}:{column} - {detailed_msg}")
        
        self.errors.append(SyntaxError(
            message=detailed_msg,
            line=line,
            column=column
        ))
    
    def get_errors(self) -> List[SyntaxError]:
        """Get all syntax errors"""
        return self.errors
    
    def has_errors(self) -> bool:
        """Check if there are any syntax errors"""
        return len(self.errors) > 0
