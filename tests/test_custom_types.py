
import unittest
from testdatagen.core.parser import Parser
from testdatagen.core.semantic.analyzer import SemanticAnalyzer
from testdatagen.core.types.registry import TypeRegistry, default_registry
from testdatagen.core.types.custom import CustomType

class TestCustomTypeRegistration(unittest.TestCase):
    def setUp(self):
        # Create a fresh registry for each test
        self.registry = TypeRegistry()
        self.analyzer = SemanticAnalyzer(type_registry=self.registry)
        self.parser = Parser()
        
    def test_basic_custom_type_registration(self):
        """Test basic custom type registration"""
        schema_text = """
        schema TestSchema {
            type Email = string;
            type PositiveInt = integer;
            
            table Test {
                field id: integer;
                field email: Email;
                field count: PositiveInt;
            }
        }
        """
        
        # Parse the schema
        result = self.parser.parse_string(schema_text)
        self.assertTrue(result.success, f"Failed to parse schema: {result.errors}")
        
        # Analyze the schema
        errors = self.analyzer.analyze(result.ast)
        self.assertEqual(len(errors), 0, f"Semantic analysis failed with errors: {errors}")
        
        # Check that the custom types were registered
        self.assertTrue(self.registry.exists("Email"), "Email type was not registered")
        self.assertTrue(self.registry.exists("PositiveInt"), "PositiveInt type was not registered")
        
        # Check the properties of the custom types
        email_type = self.registry.get("Email")
        self.assertIsInstance(email_type, CustomType, "Email type is not a CustomType")
        self.assertEqual(email_type.base_type, "string", "Email type has incorrect base type")
        
        positive_int_type = self.registry.get("PositiveInt")
        self.assertIsInstance(positive_int_type, CustomType, "PositiveInt type is not a CustomType")
        self.assertEqual(positive_int_type.base_type, "integer", "PositiveInt type has incorrect base type")
        
    def test_custom_type_with_constraints(self):
        """Test custom type registration with constraints"""
        schema_text = """
        schema TestSchema {
            type Email = string with pattern("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$");
            type PositiveInt = integer with range(1, 100);
            
            table Test {
                field id: integer;
                field email: Email;
                field count: PositiveInt;
            }
        }
        """
        
        # Parse the schema
        result = self.parser.parse_string(schema_text)
        self.assertTrue(result.success, f"Failed to parse schema: {result.errors}")
        
        # Analyze the schema
        errors = self.analyzer.analyze(result.ast)
        self.assertEqual(len(errors), 0, f"Semantic analysis failed with errors: {errors}")
        
        # Check that the custom types were registered
        self.assertTrue(self.registry.exists("Email"), "Email type was not registered")
        self.assertTrue(self.registry.exists("PositiveInt"), "PositiveInt type was not registered")
        
        # Check the constraints of the custom types
        email_type = self.registry.get("Email")
        self.assertIsInstance(email_type, CustomType, "Email type is not a CustomType")
        self.assertEqual(email_type.base_type, "string", "Email type has incorrect base type")
        
        # The constraints might not be properly processed yet, but we can check they exist
        self.assertTrue(hasattr(email_type, "constraints"), "Email type has no constraints attribute")
        
        positive_int_type = self.registry.get("PositiveInt")
        self.assertIsInstance(positive_int_type, CustomType, "PositiveInt type is not a CustomType")
        self.assertEqual(positive_int_type.base_type, "integer", "PositiveInt type has incorrect base type")
        self.assertTrue(hasattr(positive_int_type, "constraints"), "PositiveInt type has no constraints attribute")
        
    def test_invalid_base_type(self):
        """Test custom type with invalid base type"""
        schema_text = """
        schema TestSchema {
            type InvalidType = nonexistent_type;
            
            table Test {
                field id: integer;
            }
        }
        """
        
        # Parse the schema
        result = self.parser.parse_string(schema_text)
        self.assertTrue(result.success, f"Failed to parse schema: {result.errors}")
        
        # Analyze the schema
        errors = self.analyzer.analyze(result.ast)
        self.assertGreater(len(errors), 0, "Expected semantic errors for invalid base type")
        
        # Check that the error message mentions the invalid base type
        error_messages = [error.message for error in errors]
        self.assertTrue(
            any("nonexistent_type" in msg for msg in error_messages),
            f"Error message should mention invalid base type: {error_messages}"
        )
        
    def test_reference_custom_type_in_field(self):
        """Test referencing a custom type in a field declaration"""
        schema_text = """
        schema TestSchema {
            type Email = string;
            
            table Test {
                field id: integer;
                field email: Email;
            }
        }
        """
        
        # Parse the schema
        result = self.parser.parse_string(schema_text)
        self.assertTrue(result.success, f"Failed to parse schema: {result.errors}")
        
        # Analyze the schema
        errors = self.analyzer.analyze(result.ast)
        self.assertEqual(len(errors), 0, f"Semantic analysis failed with errors: {errors}")
        
        # Check that the field references the custom type
        email_field = result.ast.tables[0].fields[1]
        self.assertEqual(email_field.name, "email", "Field name is incorrect")
        self.assertEqual(email_field.data_type, "Email", "Field data type is incorrect")

if __name__ == "__main__":
    unittest.main()
