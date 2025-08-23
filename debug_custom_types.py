
#!/usr/bin/env python3

from testdatagen.core.parser import Parser
from testdatagen.core.semantic.analyzer import SemanticAnalyzer
from testdatagen.core.types.registry import default_registry

# Test file path
test_file = "examples/basic/custom_types_simple.tdg"

# Parse the file
parser = Parser()
with open(test_file, 'r') as f:
    content = f.read()
    
print(f"Parsing file: {test_file}")
print(f"File content:\n{content}")

# Create a simpler test file with just type declarations
simple_content = """
schema SimpleTypes {
    type Email = string;
    type PositiveInt = integer;
}
"""
print(f"\nSimple content:\n{simple_content}")

print("\nParsing original content:")
result = parser.parse_string(content)

if not result.success:
    print("Parsing failed with errors:")
    for error in result.errors:
        print(f"  {error.message} at line {error.line}, column {error.column}")
    exit(1)
    
ast = result.ast

# Print the raw AST structure
print("\nRaw AST Structure:")
print(f"Schema: {ast}")
print(f"Types: {ast.types}")

print("\nAST Structure:")
print(f"Schema name: {ast.name}")
print(f"Types: {[t.name for t in ast.types]}")
print(f"Tables: {[t.name for t in ast.tables]}")

# Analyze the AST
analyzer = SemanticAnalyzer()
errors = analyzer.analyze(ast)

print("\nSemantic Analysis:")
if errors:
    print(f"Found {len(errors)} errors:")
    for error in errors:
        print(f"  {error.severity.upper()} at line {error.line}, column {error.column}: {error.message}")
else:
    print("No semantic errors found")

# Check registered types
print("\nRegistered Types:")
for type_name, type_def in default_registry._types.items():
    print(f"  {type_name}: {type_def.__class__.__name__}")

# Check if custom types were registered
print("\nCustom Types:")
for type_node in ast.types:
    print(f"  {type_node.name}: base_type={type_node.base_type}, constraints={len(type_node.constraints)}")
    for constraint in type_node.constraints:
        print(f"    - {constraint.constraint_type}: {constraint.parameters}")

print("\nDone!")
