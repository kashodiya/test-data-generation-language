






















from typing import Dict, List, Optional, Any, Union, Tuple, Callable
import pandas as pd
from faker import Faker

from ...core.ast.nodes import SchemaNode, TableNode, FieldNode
from .base import GenerationStrategy


class FakerStrategy(GenerationStrategy):
    """Strategy for generating data using Faker"""
    
    def __init__(self):
        super().__init__()
        self.faker = None
        self.type_mapping = {}
        self._initialize_type_mapping()
    
    def initialize(self, schema: SchemaNode, options: Any) -> None:
        """Initialize the strategy with a schema and options"""
        super().initialize(schema, options)
        
        # Initialize Faker with locale
        locale = options.locale if hasattr(options, 'locale') else "en_US"
        self.faker = Faker(locale)
        
        # Set random seed if provided
        if hasattr(options, 'seed') and options.seed is not None:
            Faker.seed(options.seed)
    
    def _initialize_type_mapping(self) -> None:
        """Initialize the mapping of data types to Faker providers"""
        self.type_mapping = {
            # Basic types
            "integer": lambda f, _: f.random_int(min=-1000000, max=1000000),
            "decimal": lambda f, _: f.pyfloat(min_value=-1000000, max_value=1000000),
            "string": lambda f, _: f.text(max_nb_chars=50),
            "boolean": lambda f, _: f.boolean(),
            "date": lambda f, _: f.date(),
            "timestamp": lambda f, _: f.date_time().isoformat(),
            "binary": lambda f, _: f.binary(length=64),
            "uuid": lambda f, _: f.uuid4(),
            "json": lambda f, _: {"data": f.pydict(nb_elements=5)},
            
            # Common field names
            "name": lambda f, _: f.name(),
            "first_name": lambda f, _: f.first_name(),
            "last_name": lambda f, _: f.last_name(),
            "full_name": lambda f, _: f.name(),
            "email": lambda f, _: f.email(),
            "phone": lambda f, _: f.phone_number(),
            "phone_number": lambda f, _: f.phone_number(),
            "address": lambda f, _: f.address(),
            "street": lambda f, _: f.street_address(),
            "city": lambda f, _: f.city(),
            "state": lambda f, _: f.state(),
            "zip": lambda f, _: f.zipcode(),
            "zip_code": lambda f, _: f.zipcode(),
            "postal_code": lambda f, _: f.postcode(),
            "country": lambda f, _: f.country(),
            "company": lambda f, _: f.company(),
            "company_name": lambda f, _: f.company(),
            "job": lambda f, _: f.job(),
            "job_title": lambda f, _: f.job(),
            "username": lambda f, _: f.user_name(),
            "password": lambda f, _: f.password(),
            "url": lambda f, _: f.url(),
            "uri": lambda f, _: f.uri(),
            "image": lambda f, _: f.image_url(),
            "image_url": lambda f, _: f.image_url(),
            "color": lambda f, _: f.color_name(),
            "product": lambda f, _: f.catch_phrase(),
            "product_name": lambda f, _: f.catch_phrase(),
            "price": lambda f, _: f.pydecimal(min_value=1, max_value=1000, right_digits=2),
            "description": lambda f, _: f.paragraph(),
            "summary": lambda f, _: f.text(max_nb_chars=100),
            "title": lambda f, _: f.sentence(),
            "content": lambda f, _: f.paragraphs(nb=3),
            "comment": lambda f, _: f.text(),
            "rating": lambda f, _: f.random_int(min=1, max=5),
            "latitude": lambda f, _: float(f.latitude()),
            "longitude": lambda f, _: float(f.longitude()),
            "coordinates": lambda f, _: {"lat": float(f.latitude()), "lng": float(f.longitude())},
            "ip": lambda f, _: f.ipv4(),
            "ipv4": lambda f, _: f.ipv4(),
            "ipv6": lambda f, _: f.ipv6(),
            "mac_address": lambda f, _: f.mac_address(),
            "user_agent": lambda f, _: f.user_agent(),
            "ssn": lambda f, _: f.ssn(),
            "credit_card": lambda f, _: f.credit_card_number(),
            "credit_card_number": lambda f, _: f.credit_card_number(),
            "credit_card_provider": lambda f, _: f.credit_card_provider(),
            "credit_card_expire": lambda f, _: f.credit_card_expire(),
            "iban": lambda f, _: f.iban(),
            "bic": lambda f, _: f.swift(),
            "bank_account": lambda f, _: f.bban(),
            "currency": lambda f, _: f.currency_code(),
            "currency_code": lambda f, _: f.currency_code(),
            "currency_name": lambda f, _: f.currency_name(),
            "language": lambda f, _: f.language_code(),
            "language_code": lambda f, _: f.language_code(),
            "language_name": lambda f, _: f.language_name(),
            "locale": lambda f, _: f.locale(),
            "country_code": lambda f, _: f.country_code(),
            "file_name": lambda f, _: f.file_name(),
            "file_path": lambda f, _: f.file_path(),
            "mime_type": lambda f, _: f.mime_type(),
            "file_extension": lambda f, _: f.file_extension(),
            "isbn": lambda f, _: f.isbn13(),
            "isbn10": lambda f, _: f.isbn10(),
            "isbn13": lambda f, _: f.isbn13(),
        }
    
    def generate_table(self, table: TableNode, options: Any) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Generate data for a table"""
        # Get record count
        record_count = options.record_count if hasattr(options, 'record_count') else 100
        
        # Generate data
        data = []
        
        # Measure execution time
        def generate_data():
            for i in range(record_count):
                row = {}
                for field in table.fields:
                    row[field.name] = self.generate_field(field, table, i, {})
                data.append(row)
            return pd.DataFrame(data)
        
        df, execution_time_ms = self.measure_execution_time(generate_data)
        
        # Collect statistics
        stats = {
            "record_count": record_count,
            "generation_time_ms": execution_time_ms,
            "avg_time_per_record_ms": execution_time_ms / record_count if record_count > 0 else 0
        }
        
        return df, stats
    
    def generate_field(self, field: FieldNode, table: TableNode, row_index: int, context: Dict[str, Any]) -> Any:
        """Generate a value for a field"""
        # Check if field is nullable and randomly decide to return None
        if field.nullable and self.faker.random_int(min=1, max=10) == 1:  # 10% chance of NULL
            return None
        
        # Check for field-specific generation directives
        for constraint in field.constraints:
            if constraint.constraint_type == "generate":
                return self._handle_generate_directive(constraint, field)
        
        # Try to find a generator based on field name
        field_name = field.name.lower()
        if field_name in self.type_mapping:
            return self.type_mapping[field_name](self.faker, field)
        
        # Generate based on data type
        data_type = field.data_type.lower()
        
        if data_type in self.type_mapping:
            return self.type_mapping[data_type](self.faker, field)
        elif "[]" in data_type:  # Array type
            return self._generate_array(field)
        else:
            # Unknown type, return None
            return None
    
    def _handle_generate_directive(self, constraint: Any, field: FieldNode) -> Any:
        """Handle a generate directive"""
        params = constraint.parameters
        
        # Check for provider
        provider = params["provider"] if "provider" in params else None
        if not provider:
            return None
            
        # Check for method
        method = params["method"] if "method" in params else None
        if not method:
            return None
            
        # Check if provider exists
        if not hasattr(self.faker, provider):
            return None
            
        # Get provider
        faker_provider = getattr(self.faker, provider)
        
        # Check if method exists
        if not hasattr(faker_provider, method):
            return None
            
        # Get method
        faker_method = getattr(faker_provider, method)
        
        # Get arguments
        args = params["args"] if "args" in params else []
        kwargs = params["kwargs"] if "kwargs" in params else {}
        
        # Call method
        try:
            return faker_method(*args, **kwargs)
        except Exception:
            return None
    
    def _generate_array(self, field: FieldNode) -> List[Any]:
        """Generate a random array"""
        # Extract base type from array type (e.g., "string[]" -> "string")
        base_type = field.data_type.split("[")[0]
        
        # Create a temporary field with the base type
        temp_field = FieldNode(
            node_type=field.node_type,
            name=field.name,
            data_type=base_type,
            constraints=field.constraints,
            nullable=field.nullable,
            line=field.line,
            column=field.column
        )
        
        # Generate array elements
        length = self.faker.random_int(min=0, max=5)
        return [self.generate_field(temp_field, None, i, {}) for i in range(length)]






















