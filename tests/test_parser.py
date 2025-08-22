









import unittest
import os
from pathlib import Path

from testdatagen.core.parser import Parser


class TestParser(unittest.TestCase):
    """Test the parser module"""
    
    def setUp(self):
        self.parser = Parser()
        self.examples_dir = Path(__file__).parent.parent / "examples"
    
    def test_parse_basic_schema(self):
        """Test parsing a basic schema"""
        schema_file = self.examples_dir / "basic" / "simple_table.tdg"
        
        # Skip if file doesn't exist
        if not schema_file.exists():
            self.skipTest(f"Schema file {schema_file} does not exist")
        
        result = self.parser.parse_file(str(schema_file))
        
        self.assertTrue(result.success, f"Parsing failed with errors: {result.errors}")
        self.assertIsNotNone(result.ast)
        self.assertEqual(result.ast.name, "TestDatabase")
        self.assertEqual(len(result.ast.tables), 4)
        
        # Check User table
        user_table = next((t for t in result.ast.tables if t.name == "User"), None)
        self.assertIsNotNone(user_table)
        self.assertEqual(len(user_table.fields), 8)
        
        # Check Product table
        product_table = next((t for t in result.ast.tables if t.name == "Product"), None)
        self.assertIsNotNone(product_table)
        self.assertEqual(len(product_table.fields), 7)
    
    def test_parse_advanced_schema(self):
        """Test parsing an advanced schema with custom types"""
        schema_file = self.examples_dir / "advanced" / "custom_types.tdg"
        
        # Skip if file doesn't exist
        if not schema_file.exists():
            self.skipTest(f"Schema file {schema_file} does not exist")
        
        result = self.parser.parse_file(str(schema_file))
        
        self.assertTrue(result.success, f"Parsing failed with errors: {result.errors}")
        self.assertIsNotNone(result.ast)
        self.assertEqual(result.ast.name, "AdvancedExample")
        self.assertEqual(len(result.ast.tables), 5)
        
        # Check Customer table
        customer_table = next((t for t in result.ast.tables if t.name == "Customer"), None)
        self.assertIsNotNone(customer_table)
        self.assertEqual(len(customer_table.fields), 8)
        
        # Check Product table
        product_table = next((t for t in result.ast.tables if t.name == "Product"), None)
        self.assertIsNotNone(product_table)
        self.assertEqual(len(product_table.fields), 10)


if __name__ == "__main__":
    unittest.main()









