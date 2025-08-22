










from typing import List
from antlr4.error.ErrorListener import ErrorListener
from pydantic import BaseModel


class SyntaxError(BaseModel):
    """Represents a syntax error"""
    message: str
    line: int
    column: int
    severity: str = "error"


class TestDataGenErrorListener(ErrorListener):
    """Custom error listener for ANTLR"""
    
    def __init__(self):
        super().__init__()
        self.errors: List[SyntaxError] = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """Called when a syntax error occurs"""
        self.errors.append(SyntaxError(
            message=msg,
            line=line,
            column=column
        ))
    
    def get_errors(self) -> List[SyntaxError]:
        """Get all syntax errors"""
        return self.errors
    
    def has_errors(self) -> bool:
        """Check if there are any syntax errors"""
        return len(self.errors) > 0










