











import unittest
import os
from pathlib import Path

from testdatagen.core.parser import Parser
from testdatagen.generator.engine import GenerationEngine, GenerationOptions
from testdatagen.generator.strategies.random_strategy import RandomStrategy
from testdatagen.generator.strategies.faker_strategy import FakerStrategy


class TestGenerator(unittest.TestCase):
    """Test the generator module"""
    
    def setUp(self):
        self.parser = Parser()
        self.examples_dir = Path(__file__).parent.parent / "examples"
        
        # Initialize strategies
        self.strategies = {
            "random": RandomStrategy(),
            "faker": FakerStrategy()
        }
        
        # Initialize engine
        self.engine = GenerationEngine(self.strategies)
    
    def test_generate_basic_schema(self):
        """Test generating data for a basic schema"""
        schema_file = self.examples_dir / "basic" / "simple_table.tdg"
        
        # Skip if file doesn't exist
        if not schema_file.exists():
            self.skipTest(f"Schema file {schema_file} does not exist")
        
        # Parse schema
        parse_result = self.parser.parse_file(str(schema_file))
        self.assertTrue(parse_result.success, f"Parsing failed with errors: {parse_result.errors}")
        
        # Set up generation options
        options = GenerationOptions(
            record_count=10,
            seed=12345,
            strategy="random"
        )
        
        # Generate data
        result = self.engine.generate(parse_result.ast, options)
        
        # Check result
        self.assertTrue(result.success, f"Generation failed with errors: {result.errors}")
        self.assertIsNotNone(result.data)
        self.assertEqual(len(result.data), 4)  # 4 tables
        
        # Check User table
        self.assertIn("User", result.data)
        self.assertEqual(len(result.data["User"]), 10)  # 10 records
        
        # Check Product table
        self.assertIn("Product", result.data)
        self.assertEqual(len(result.data["Product"]), 10)  # 10 records
    
    def test_generate_with_faker_strategy(self):
        """Test generating data with the Faker strategy"""
        schema_file = self.examples_dir / "basic" / "simple_table.tdg"
        
        # Skip if file doesn't exist
        if not schema_file.exists():
            self.skipTest(f"Schema file {schema_file} does not exist")
        
        # Parse schema
        parse_result = self.parser.parse_file(str(schema_file))
        self.assertTrue(parse_result.success, f"Parsing failed with errors: {parse_result.errors}")
        
        # Set up generation options
        options = GenerationOptions(
            record_count=10,
            seed=12345,
            strategy="faker"
        )
        
        # Generate data
        result = self.engine.generate(parse_result.ast, options)
        
        # Check result
        self.assertTrue(result.success, f"Generation failed with errors: {result.errors}")
        self.assertIsNotNone(result.data)
        self.assertEqual(len(result.data), 4)  # 4 tables
        
        # Check User table
        self.assertIn("User", result.data)
        self.assertEqual(len(result.data["User"]), 10)  # 10 records
        
        # Check that email fields look like emails
        for user in result.data["User"].to_dict('records'):
            if user["email"] is not None:
                self.assertIn("@", user["email"], f"Email {user['email']} does not look like an email")


if __name__ == "__main__":
    unittest.main()











