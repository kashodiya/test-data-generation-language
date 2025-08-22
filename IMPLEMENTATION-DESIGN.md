# DSL for Test Data Generation - Python Implementation Plan

## Document Information
- **Version**: 1.0
- **Date**: August 21, 2025
- **Project**: TestDataGen DSL Implementation Plan (Python)
- **Status**: Draft

## 1. Technology Stack Selection

### 1.1 Core Language Choice: **Python 3.11+**

**Rationale:**
- **Rich Ecosystem**: Extensive libraries for data manipulation and testing
- **Rapid Development**: Faster prototyping and iteration cycles
- **Data Science Integration**: Native support for pandas, numpy for large datasets
- **Community**: Large developer community familiar with testing frameworks
- **Faker Integration**: Native Python Faker library with extensive providers
- **Database Libraries**: Mature ORM and database connectivity options

**Version Choice**: Python 3.11+ for improved performance and type hinting features

### 1.2 Parser Generator: **ANTLR4 with Python Runtime**

**Rationale:**
- **Mature Technology**: Battle-tested with excellent Python support
- **Grammar Reusability**: Grammar files can be shared across language implementations
- **Tool Ecosystem**: ANTLRWorks for grammar visualization and debugging
- **Error Recovery**: Good error handling and recovery mechanisms
- **Tree Walkers**: Built-in visitor and listener patterns

**Alternative**: Lark (considered but ANTLR4 chosen for enterprise-grade features)

### 1.3 Code Generation: **Jinja2 Templates**

**Rationale:**
- **Industry Standard**: Widely adopted templating engine
- **Feature Rich**: Inheritance, macros, filters, and control structures
- **Security**: Auto-escaping and sandbox mode
- **Performance**: Compiled templates with good caching
- **Ecosystem**: Extensive filter library and community extensions

### 1.4 Database Integration: **SQLAlchemy 2.0 + Alembic**

**Rationale:**
- **Mature ORM**: Industry standard for Python database operations
- **Multi-database**: PostgreSQL, MySQL, SQLite, Oracle, SQL Server support
- **Type Safety**: Full type hint support in SQLAlchemy 2.0
- **Migration Support**: Alembic for schema evolution
- **Connection Pooling**: Built-in connection management
- **Async Support**: Full async/await support

### 1.5 CLI Framework: **Click + Rich**

**Rationale:**
- **Click**: De facto standard for Python CLIs
- **Rich**: Beautiful terminal output with progress bars, tables, syntax highlighting
- **Composability**: Easy command grouping and parameter handling
- **Testing**: Excellent testing support with ClickTesting
- **Auto-completion**: Built-in shell completion support

### 1.6 Data Manipulation: **pandas + NumPy**

**Rationale:**
- **Performance**: Optimized data operations for large datasets
- **Memory Efficiency**: Efficient data structures and operations
- **Export Formats**: Native support for CSV, JSON, Parquet, Excel
- **Data Types**: Rich type system including datetime, categorical data
- **Integration**: Works seamlessly with database connectors

### 1.7 Testing Framework: **pytest + hypothesis**

**Rationale:**
- **pytest**: Most popular Python testing framework
- **hypothesis**: Property-based testing for robust validation
- **Fixtures**: Excellent dependency injection and setup/teardown
- **Plugins**: Rich plugin ecosystem
- **Coverage**: Integration with coverage.py

### 1.8 Type Checking: **mypy + pydantic**

**Rationale:**
- **mypy**: Static type checking for Python
- **pydantic**: Runtime validation and serialization with type hints
- **Data Classes**: Built-in support for dataclasses and attrs
- **IDE Support**: Excellent integration with modern IDEs

### 1.9 Async Framework: **asyncio + aiofiles**

**Rationale:**
- **Built-in**: Native Python async support
- **Performance**: Non-blocking I/O for database and file operations
- **Ecosystem**: Mature async ecosystem with database drivers
- **Compatibility**: Works with modern Python web frameworks

## 2. Project Architecture

### 2.1 Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                       │
├─────────────────────┬─────────────────┬─────────────────────┤
│      CLI Tool       │   Web API       │   Jupyter Plugin    │
├─────────────────────┼─────────────────┼─────────────────────┤
│                     Service Layer                          │
├─────────────────────┼─────────────────┼─────────────────────┤
│  Generator Engine   │  Template Eng.  │  Export Handlers    │
├─────────────────────┼─────────────────┼─────────────────────┤
│                      Core Layer                            │
├─────────────────────┼─────────────────┼─────────────────────┤
│     Parser          │   AST Model     │   Type System       │
├─────────────────────┼─────────────────┼─────────────────────┤
│                  Infrastructure Layer                      │
├─────────────────────┼─────────────────┼─────────────────────┤
│   File System      │    Database     │   Network I/O       │
└─────────────────────┴─────────────────┴─────────────────────┘
```

### 2.2 Package Structure

```python
testdatagen/
├── pyproject.toml              # Project configuration (PEP 621)
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── .github/                    # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml
│       ├── release.yml
│       └── docs.yml
├── src/                        # Source code (src layout)
│   └── testdatagen/
│       ├── __init__.py
│       ├── core/               # Core DSL functionality
│       │   ├── __init__.py
│       │   ├── ast/            # Abstract Syntax Tree
│       │   │   ├── __init__.py
│       │   │   ├── nodes.py    # AST node definitions
│       │   │   ├── schema.py   # Schema-specific nodes
│       │   │   ├── table.py    # Table-specific nodes
│       │   │   └── field.py    # Field-specific nodes
│       │   ├── parser/         # ANTLR4 parser
│       │   │   ├── __init__.py
│       │   │   ├── grammar/    # Grammar files
│       │   │   │   ├── TestDataGen.g4
│       │   │   │   └── TestDataGenLexer.g4
│       │   │   ├── generated/  # ANTLR generated files
│       │   │   ├── builder.py  # AST builder from parse tree
│       │   │   └── error_listener.py
│       │   ├── types/          # Type system
│       │   │   ├── __init__.py
│       │   │   ├── primitive.py
│       │   │   ├── composite.py
│       │   │   ├── custom.py
│       │   │   └── registry.py
│       │   ├── constraints/    # Constraint system
│       │   │   ├── __init__.py
│       │   │   ├── base.py     # Base constraint classes
│       │   │   ├── value.py    # Value constraints
│       │   │   ├── business.py # Business rule constraints
│       │   │   └── relationship.py
│       │   └── semantic/       # Semantic analysis
│       │       ├── __init__.py
│       │       ├── analyzer.py
│       │       ├── symbol_table.py
│       │       ├── type_checker.py
│       │       └── validator.py
│       ├── generator/          # Data generation engine
│       │   ├── __init__.py
│       │   ├── engine.py       # Main generation engine
│       │   ├── strategies/     # Generation strategies
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   ├── random_strategy.py
│       │   │   ├── faker_strategy.py
│       │   │   ├── pattern_strategy.py
│       │   │   └── sequential_strategy.py
│       │   ├── providers/      # Data providers
│       │   │   ├── __init__.py
│       │   │   ├── faker_provider.py
│       │   │   ├── custom_provider.py
│       │   │   ├── lookup_provider.py
│       │   │   └── dataset_provider.py
│       │   ├── relationships/  # Relationship handling
│       │   │   ├── __init__.py
│       │   │   ├── foreign_key.py
│       │   │   ├── dependency_graph.py
│       │   │   └── reference_resolver.py
│       │   └── batch/          # Batch processing
│       │       ├── __init__.py
│       │       ├── processor.py
│       │       └── memory_manager.py
│       ├── export/             # Output format handlers
│       │   ├── __init__.py
│       │   ├── base.py         # Base exporter
│       │   ├── formats/
│       │   │   ├── __init__.py
│       │   │   ├── sql.py
│       │   │   ├── json_format.py
│       │   │   ├── csv_format.py
│       │   │   ├── excel.py
│       │   │   ├── parquet_format.py
│       │   │   └── xml_format.py
│       │   └── database/
│       │       ├── __init__.py
│       │       ├── base.py
│       │       ├── postgres.py
│       │       ├── mysql.py
│       │       ├── sqlite.py
│       │       └── sqlserver.py
│       ├── cli/                # Command line interface
│       │   ├── __init__.py
│       │   ├── main.py         # Main CLI entry point
│       │   ├── commands/
│       │   │   ├── __init__.py
│       │   │   ├── generate.py
│       │   │   ├── validate.py
│       │   │   ├── schema.py
│       │   │   └── server.py
│       │   ├── config.py
│       │   └── utils.py
│       ├── web/                # Web API (FastAPI)
│       │   ├── __init__.py
│       │   ├── app.py          # FastAPI application
│       │   ├── routers/
│       │   │   ├── __init__.py
│       │   │   ├── generation.py
│       │   │   ├── validation.py
│       │   │   └── schema.py
│       │   ├── models/         # Pydantic models
│       │   │   ├── __init__.py
│       │   │   ├── request.py
│       │   │   └── response.py
│       │   └── dependencies.py
│       ├── lsp/                # Language Server Protocol
│       │   ├── __init__.py
│       │   ├── server.py       # LSP server implementation
│       │   ├── handlers/
│       │   │   ├── __init__.py
│       │   │   ├── completion.py
│       │   │   ├── diagnostics.py
│       │   │   ├── hover.py
│       │   │   └── definition.py
│       │   └── protocol.py
│       ├── plugins/            # Plugin system
│       │   ├── __init__.py
│       │   ├── api/            # Plugin API
│       │   │   ├── __init__.py
│       │   │   ├── generator.py
│       │   │   ├── provider.py
│       │   │   └── exporter.py
│       │   ├── loader.py       # Plugin loader
│       │   └── registry.py     # Plugin registry
│       └── utils/              # Utilities
│           ├── __init__.py
│           ├── logging.py
│           ├── config.py
│           ├── exceptions.py
│           └── helpers.py
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── unit/                   # Unit tests
│   │   ├── test_parser.py
│   │   ├── test_types.py
│   │   ├── test_constraints.py
│   │   ├── test_generator.py
│   │   └── test_export.py
│   ├── integration/            # Integration tests
│   │   ├── test_cli.py
│   │   ├── test_database.py
│   │   ├── test_workflows.py
│   │   └── test_performance.py
│   ├── fixtures/               # Test data
│   │   ├── schemas/
│   │   ├── expected_outputs/
│   │   └── sample_data/
│   └── conftest.py             # pytest configuration
├── docs/                       # Documentation
│   ├── conf.py                 # Sphinx configuration
│   ├── index.rst
│   ├── installation.rst
│   ├── quickstart.rst
│   ├── language-reference/
│   │   ├── index.rst
│   │   ├── types.rst
│   │   ├── constraints.rst
│   │   └── grammar.rst
│   ├── examples/
│   │   ├── index.rst
│   │   ├── basic.rst
│   │   ├── relationships.rst
│   │   └── advanced.rst
│   ├── api/
│   │   ├── index.rst
│   │   └── modules.rst
│   └── _static/
├── examples/                   # Example DSL files
│   ├── basic/
│   │   ├── simple_table.tdg
│   │   ├── with_constraints.tdg
│   │   └── README.md
│   ├── relationships/
│   │   ├── foreign_keys.tdg
│   │   ├── many_to_many.tdg
│   │   └── README.md
│   └── advanced/
│       ├── custom_generators.tdg
│       ├── business_rules.tdg
│       └── README.md
├── notebooks/                  # Jupyter notebooks
│   ├── getting_started.ipynb
│   ├── advanced_examples.ipynb
│   └── performance_analysis.ipynb
├── tools/                      # Development tools
│   ├── grammar_check.py
│   ├── benchmark.py
│   ├── generate_antlr.py
│   └── release.py
├── benchmarks/                 # Performance benchmarks
│   ├── __init__.py
│   ├── generation_speed.py
│   ├── memory_usage.py
│   └── scalability.py
└── integrations/               # Framework integrations
    ├── pytest_plugin/
    │   ├── __init__.py
    │   ├── plugin.py
    │   └── fixtures.py
    ├── unittest_integration/
    ├── django_integration/
    └── flask_integration/
```

### 2.3 pyproject.toml Configuration

```toml
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "testdatagen"
version = "0.1.0"
description = "Domain-Specific Language for Test Data Generation"
authors = [{name = "TestDataGen Team", email = "team@testdatagen.dev"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11"
keywords = ["testing", "data-generation", "dsl", "faker"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Testing",
    "Topic :: Database",
]

dependencies = [
    # Core dependencies
    "antlr4-python3-runtime>=4.13.0",
    "pydantic>=2.5.0",
    "jinja2>=3.1.0",
    
    # Data manipulation
    "pandas>=2.1.0",
    "numpy>=1.24.0",
    "pyarrow>=13.0.0",  # For Parquet support
    
    # Database
    "sqlalchemy[asyncio]>=2.0.0",
    "alembic>=1.12.0",
    "asyncpg>=0.29.0",      # PostgreSQL async
    "aiomysql>=0.2.0",      # MySQL async
    "aiosqlite>=0.19.0",    # SQLite async
    
    # CLI and UI
    "click>=8.1.0",
    "rich>=13.6.0",
    "typer>=0.9.0",         # Alternative to Click with type hints
    
    # Data generation
    "faker>=20.0.0",
    
    # Web API
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    
    # Language Server
    "pygls>=1.1.0",         # Generic Language Server
    
    # Utilities
    "pyyaml>=6.0.1",
    "toml>=0.10.2",
    "python-dotenv>=1.0.0",
    "aiofiles>=23.2.0",
]

[project.optional-dependencies]
dev = [
    # Testing
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "hypothesis>=6.88.0",
    
    # Code quality
    "black>=23.9.0",
    "ruff>=0.1.0",          # Fast linter (replaces flake8, isort)
    "mypy>=1.6.0",
    "pre-commit>=3.5.0",
    
    # Documentation
    "sphinx>=7.2.0",
    "sphinx-rtd-theme>=1.3.0",
    "sphinx-autodoc-typehints>=1.24.0",
    
    # Development tools
    "ipython>=8.16.0",
    "jupyter>=1.0.0",
]

web = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "python-multipart>=0.0.6",
]

lsp = [
    "pygls>=1.1.0",
]

all = [
    "testdatagen[dev,web,lsp]"
]

[project.urls]
Homepage = "https://github.com/testdatagen/testdatagen"
Documentation = "https://testdatagen.readthedocs.io"
Repository = "https://github.com/testdatagen/testdatagen"
Changelog = "https://github.com/testdatagen/testdatagen/blob/main/CHANGELOG.md"

[project.scripts]
testdatagen = "testdatagen.cli.main:main"
tdg = "testdatagen.cli.main:main"
testdatagen-lsp = "testdatagen.lsp.server:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
target-version = "py311"
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=testdatagen",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

[tool.coverage.run]
source = ["testdatagen"]
omit = [
    "tests/*",
    "*/generated/*",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## 3. Development Phases

### 3.1 Phase 1: Foundation (Months 1-3)

#### 3.1.1 Month 1: Project Setup and Core Parser

**Deliverables:**
- Project structure with modern Python tooling
- ANTLR4 grammar for basic DSL syntax
- Basic AST nodes with pydantic models
- CLI scaffolding with Click and Rich

**Key Components:**
```python
# src/testdatagen/core/ast/nodes.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class NodeType(str, Enum):
    SCHEMA = "schema"
    TABLE = "table"
    FIELD = "field"
    CONSTRAINT = "constraint"

class ASTNode(BaseModel):
    """Base class for all AST nodes"""
    node_type: NodeType
    line: int = Field(description="Line number in source")
    column: int = Field(description="Column number in source")

class FieldNode(ASTNode):
    name: str
    data_type: str
    constraints: List['ConstraintNode'] = Field(default_factory=list)
    nullable: bool = True
    default_value: Optional[Any] = None

class TableNode(ASTNode):
    name: str
    fields: List[FieldNode]
    constraints: List['ConstraintNode'] = Field(default_factory=list)

class SchemaNode(ASTNode):
    name: str
    tables: List[TableNode]
    imports: List[str] = Field(default_factory=list)
```

#### 3.1.2 Month 2: Type System and Semantic Analysis

**Deliverables:**
- Complete type system with pydantic validation
- Constraint validation framework
- Symbol table and scope resolution
- Comprehensive error reporting

**Key Components:**
```python
# src/testdatagen/core/types/primitive.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Union, Any
from abc import ABC, abstractmethod

class DataType(BaseModel, ABC):
    """Base class for all data types"""
    
    @abstractmethod
    def validate_value(self, value: Any) -> bool:
        """Validate that a value conforms to this type"""
        pass
    
    @abstractmethod
    def generate_value(self, faker_instance: Any, **kwargs) -> Any:
        """Generate a value of this type"""
        pass

class IntegerType(DataType):
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    
    def validate_value(self, value: Any) -> bool:
        if not isinstance(value, int):
            return False
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True
    
    def generate_value(self, faker_instance: Any, **kwargs) -> int:
        return faker_instance.random_int(
            min=self.min_value or 0,
            max=self.max_value or 2**31 - 1
        )

class StringType(DataType):
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    format: Optional[str] = None  # email, url, phone, etc.
    
    def validate_value(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        if self.min_length is not None and len(value) < self.min_length:
            return False
        if self.max_length is not None and len(value) > self.max_length:
            return False
        # Pattern validation would go here
        return True
    
    def generate_value(self, faker_instance: Any, **kwargs) -> str:
        if self.format == "email":
            return faker_instance.email()
        elif self.format == "phone":
            return faker_instance.phone_number()
        elif self.pattern:
            return faker_instance.bothify(self.pattern)
        else:
            length = faker_instance.random_int(
                min=self.min_length or 5,
                max=self.max_length or 50
            )
            return faker_instance.text(max_nb_chars=length)
```

#### 3.1.3 Month 3: Basic Data Generation

**Deliverables:**
- Simple data generation for primitive types
- Faker integration for realistic data
- CSV/JSON output support
- Basic CLI functionality

**Key Components:**
```python
# src/testdatagen/generator/engine.py
import pandas as pd
from faker import Faker
from typing import Dict, List, Any, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

class GenerationEngine:
    """Main data generation engine"""
    
    def __init__(self, locale: str = 'en_US', seed: Optional[int] = None):
        self.faker = Faker(locale)
        if seed:
            Faker.seed(seed)
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
    
    async def generate_table_data(
        self,
        table_schema: TableNode,
        record_count: int,
        batch_size: int = 10000
    ) -> pd.DataFrame:
        """Generate data for a single table"""
        
        # Generate data in batches for memory efficiency
        all_data = []
        
        for batch_start in range(0, record_count, batch_size):
            current_batch_size = min(batch_size, record_count - batch_start)
            
            # Generate batch data in parallel
            batch_data = await self._generate_batch(
                table_schema, current_batch_size
            )
            all_data.append(batch_data)
        
        return pd.concat(all_data, ignore_index=True)
    
    async def _generate_batch(
        self, table_schema: TableNode, count: int
    ) -> pd.DataFrame:
        """Generate a batch of data"""
        
        # Use thread pool for CPU-intensive generation
        loop = asyncio.get_event_loop()
        batch_data = await loop.run_in_executor(
            self.thread_pool, self._generate_batch_sync, table_schema, count
        )
        
        return pd.DataFrame(batch_data)
    
    def _generate_batch_sync(
        self, table_schema: TableNode, count: int
    ) -> List[Dict[str, Any]]:
        """Synchronous batch generation"""
        data = []
        
        for _ in range(count):
            record = {}
            for field in table_schema.fields:
                record[field.name] = self._generate_field_value(field)
            data.append(record)
        
        return data
    
    def _generate_field_value(self, field: FieldNode) -> Any:
        """Generate value for a single field"""
        # This would dispatch to appropriate type-specific generators
        # For now, simplified implementation
        if field.data_type == "integer":
            return self.faker.random_int()
        elif field.data_type == "string":
            return self.faker.text(max_nb_chars=50)
        elif field.data_type == "email":
            return self.faker.email()
        elif field.data_type == "datetime":
            return self.faker.date_time()
        else:
            return None
```

### 3.2 Phase 2: Advanced Generation (Months 4-6)

#### 3.2.1 Month 4: Generation Strategies and Faker Integration

**Deliverables:**
- Multiple generation strategies (random, sequential, pattern-based)
- Enhanced Faker integration with custom providers
- Distribution controls and weighted random selection
- Custom generator functions

**Key Components:**
```python
# src/testdatagen/generator/strategies/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class GenerationStrategy(ABC):
    """Base class for all generation strategies"""
    
    @abstractmethod
    def generate(
        self,
        data_type: str,
        constraints: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Any:
        """Generate a value according to this strategy"""
        pass

# src/testdatagen/generator/strategies/faker_strategy.py
from faker import Faker
from faker.providers import BaseProvider
import random
from typing import Any, Dict, List

class CustomBusinessProvider(BaseProvider):
    """Custom Faker provider for business-specific data"""
    
    def product_code(self) -> str:
        """Generate a product code like 'PRD-12345'"""
        return f"PRD-{self.random_int(10000, 99999)}"
    
    def business_email(self, domain: str = "company.com") -> str:
        """Generate business email addresses"""
        first = self.generator.first_name().lower()
        last = self.generator.last_name().lower()
        return f"{first}.{last}@{domain}"

class FakerStrategy(GenerationStrategy):
    """Strategy using Faker library for realistic data"""
    
    def __init__(self, locale: str = 'en_US', custom_providers: List = None):
        self.faker = Faker(locale)
        
        # Add custom providers
        if custom_providers:
            for provider in custom_providers:
                self.faker.add_provider(provider)
        else:
            self.faker.add_provider(CustomBusinessProvider)
    
    def generate(
        self,
        data_type: str,
        constraints: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Any:
        """Generate realistic data using Faker"""
        
        # Handle format-specific generation
        if 'format' in constraints:
            format_type = constraints['format']
            
            if format_type == 'email':
                return self.faker.email()
            elif format_type == 'phone':
                return self.faker.phone_number()
            elif format_type == 'name':
                return self.faker.name()
            elif format_type == 'address':
                return self.faker.address()
            elif format_type == 'company':
                return self.faker.company()
            elif format_type == 'product_code':
                return self.faker.product_code()
            elif format_type == 'business_email':
                domain = constraints.get('domain', 'company.com')
                return self.faker.business_email(domain)
        
        # Handle data type specific generation
        if data_type == 'string':
            min_len = constraints.get('min_length', 5)
            max_len = constraints.get('max_length', 50)
            length = random.randint(min_len, max_len)
            
            if 'pattern' in constraints:
                return self.faker.bothify(constraints['pattern'])
            else:
                return self.faker.text(max_nb_chars=length).strip()
        
        elif data_type == 'integer':
            min_val = constraints.get('min_value', 0)
            max_val = constraints.get('max_value', 2**31 - 1)
            return self.faker.random_int(min=min_val, max=max_val)
        
        elif data_type == 'decimal':
            min_val = constraints.get('min_value', 0.0)
            max_val = constraints.get('max_value', 999999.99)
            precision = constraints.get('precision', 2)
            return round(self.faker.pyfloat(min_value=min_val, max_value=max_val), precision)
        
        elif data_type == 'boolean':
            return self.faker.boolean()
        
        elif data_type == 'datetime':
            start_date = constraints.get('start_date', '-1y')
            end_date = constraints.get('end_date', 'now')
            return self.faker.date_time_between(start_date=start_date, end_date=end_date)
        
        elif data_type == 'date':
            start_date = constraints.get('start_date', '-1y')
            end_date = constraints.get('end_date', 'today')
            return self.faker.date_between(start_date=start_date, end_date=end_date)
        
        else:
            return self.faker.text(max_nb_chars=20)

# src/testdatagen/generator/strategies/weighted_strategy.py
import random
from typing import List, Tuple, Any, Dict

class WeightedRandomStrategy(GenerationStrategy):
    """Strategy for weighted random value selection"""
    
    def __init__(self, choices: List[Tuple[Any, float]]):
        """
        Initialize with weighted choices
        Args:
            choices: List of (value, weight) tuples
        """
        self.choices = choices
        self.total_weight = sum(weight for _, weight in choices)
    
    def generate(
        self,
        data_type: str,
        constraints: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Any:
        """Generate a weighted random value"""
        rand_val = random.uniform(0, self.total_weight)
        cumulative_weight = 0
        
        for value, weight in self.choices:
            cumulative_weight += weight
            if rand_val <= cumulative_weight:
                return value
        
        # Fallback to last choice
        return self.choices[-1][0]
```

#### 3.2.2 Month 5: Relationships and Dependencies

**Deliverables:**
- Foreign key relationship handling
- Dependency graph resolution
- Referential integrity maintenance
- Circular dependency detection

**Key Components:**
```python
# src/testdatagen/generator/relationships/dependency_graph.py
from typing import Dict, List, Set
from collections import defaultdict, deque
import networkx as nx  # For graph algorithms
from ..exceptions import CircularDependencyError

class DependencyGraph:
    """Manages dependencies between tables for generation order"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.foreign_keys: Dict[str, List[Dict]] = defaultdict(list)
    
    def add_table(self, table_name: str):
        """Add a table to the dependency graph"""
        self.graph.add_node(table_name)
    
    def add_foreign_key(
        self,
        source_table: str,
        source_field: str,
        target_table: str,
        target_field: str
    ):
        """Add a foreign key relationship"""
        # Source table depends on target table
        self.graph.add_edge(target_table, source_table)
        
        self.foreign_keys[source_table].append({
            'source_field': source_field,
            'target_table': target_table,
            'target_field': target_field
        })
    
    def get_generation_order(self) -> List[str]:
        """Get the order in which tables should be generated"""
        try:
            # Topological sort to handle dependencies
            return list(nx.topological_sort(self.graph))
        except nx.NetworkXError:
            # Detect circular dependencies
            cycles = list(nx.simple_cycles(self.graph))
            raise CircularDependencyError(f"Circular dependencies detected: {cycles}")
    
    def get_dependencies(self, table_name: str) -> List[str]:
        """Get direct dependencies of a table"""
        return list(self.graph.predecessors(table_name))
    
    def get_dependents(self, table_name: str) -> List[str]:
        """Get tables that depend on this table"""
        return list(self.graph.successors(table_name))

# src/testdatagen/generator/relationships/reference_resolver.py
import pandas as pd
from typing import Dict, Any, Optional, List
import random

class ReferenceResolver:
    """Resolves foreign key references during generation"""
    
    def __init__(self):
        self.generated_data: Dict[str, pd.DataFrame] = {}
        self.primary_key_caches: Dict[str, List[Any]] = {}
    
    def register_generated_data(self, table_name: str, data: pd.DataFrame):
        """Register generated data for a table"""
        self.generated_data[table_name] = data
        
        # Cache primary key values for quick lookup
        if 'id' in data.columns:  # Assuming 'id' is primary key
            self.primary_key_caches[table_name] = data['id'].tolist()
    
    def resolve_foreign_key(
        self,
        target_table: str,
        target_field: str = 'id',
        distribution: str = 'uniform'
    ) -> Any:
        """Resolve a foreign key reference"""
        if target_table not in self.generated_data:
            raise ValueError(f"Target table {target_table} not yet generated")
        
        target_data = self.generated_data[target_table]
        
        if target_field not in target_data.columns:
            raise ValueError(f"Target field {target_field} not found in {target_table}")
        
        available_values = target_data[target_field].tolist()
        
        if not available_values:
            raise ValueError(f"No values available in {target_table}.{target_field}")
        
        # Handle different distribution strategies
        if distribution == 'uniform':
            return random.choice(available_values)
        elif distribution == 'zipf':
            # Zipf distribution favors earlier values
            weights = [1.0 / (i + 1) for i in range(len(available_values))]
            return random.choices(available_values, weights=weights)[0]
        elif distribution == 'normal':
            # Normal distribution around middle values
            mid_point = len(available_values) // 2
            weights = [
                1.0 / (1 + abs(i - mid_point)) 
                for i in range(len(available_values))
            ]
            return random.choices(available_values, weights=weights)[0]
        else:
            return random.choice(available_values)

# src/testdatagen/generator/relationships/foreign_key.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from ..strategies.base import GenerationStrategy

class ForeignKeyStrategy(GenerationStrategy):
    """Strategy for generating foreign key values"""
    
    def __init__(self, reference_resolver: ReferenceResolver):
        self.resolver = reference_resolver
    
    def generate(
        self,
        data_type: str,
        constraints: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Any:
        """Generate a foreign key value"""
        
        target_table = constraints.get('references_table')
        target_field = constraints.get('references_field', 'id')
        distribution = constraints.get('distribution', 'uniform')
        
        if not target_table:
            raise ValueError("Foreign key constraint must specify target table")
        
        return self.resolver.resolve_foreign_key(
            target_table=target_table,
            target_field=target_field,
            distribution=distribution
        )
```

#### 3.2.3 Month 6: Performance Optimization

**Deliverables:**
- Parallel generation support using asyncio and multiprocessing
- Memory-efficient streaming with pandas chunks
- Batch processing optimization
- Performance benchmarking suite

**Key Components:**
```python
# src/testdatagen/generator/batch/processor.py
import asyncio
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import pandas as pd
from typing import List, Dict, Any, AsyncGenerator, Optional
import psutil
import gc

class BatchProcessor:
    """High-performance batch processing for large datasets"""
    
    def __init__(
        self,
        max_workers: Optional[int] = None,
        memory_limit_gb: float = 2.0,
        use_multiprocessing: bool = True
    ):
        self.max_workers = max_workers or min(mp.cpu_count(), 8)
        self.memory_limit_bytes = memory_limit_gb * 1024 * 1024 * 1024
        self.use_multiprocessing = use_multiprocessing
        
        if use_multiprocessing:
            self.executor = ProcessPoolExecutor(max_workers=self.max_workers)
        else:
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
    
    async def generate_large_dataset(
        self,
        table_schema: 'TableNode',
        total_records: int,
        batch_size: Optional[int] = None
    ) -> AsyncGenerator[pd.DataFrame, None]:
        """Generate large dataset in batches to manage memory"""
        
        if batch_size is None:
            batch_size = self._calculate_optimal_batch_size(table_schema, total_records)
        
        # Process batches in parallel while yielding results
        semaphore = asyncio.Semaphore(self.max_workers * 2)  # Limit concurrent batches
        
        async def generate_batch(start_idx: int, count: int) -> pd.DataFrame:
            async with semaphore:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    self.executor,
                    self._generate_batch_sync,
                    table_schema,
                    count,
                    start_idx
                )
        
        # Generate batches concurrently
        tasks = []
        for batch_start in range(0, total_records, batch_size):
            current_batch_size = min(batch_size, total_records - batch_start)
            task = generate_batch(batch_start, current_batch_size)
            tasks.append(task)
            
            # Yield completed batches as they finish
            if len(tasks) >= self.max_workers:
                for completed_task in asyncio.as_completed(tasks):
                    batch_df = await completed_task
                    yield batch_df
                    
                    # Force garbage collection to manage memory
                    gc.collect()
                
                tasks = []
        
        # Handle remaining tasks
        if tasks:
            for completed_task in asyncio.as_completed(tasks):
                yield await completed_task
    
    def _calculate_optimal_batch_size(
        self, table_schema: 'TableNode', total_records: int
    ) -> int:
        """Calculate optimal batch size based on available memory and schema complexity"""
        
        # Estimate memory per record based on field types
        estimated_bytes_per_record = 0
        for field in table_schema.fields:
            if field.data_type in ['integer', 'boolean']:
                estimated_bytes_per_record += 8
            elif field.data_type in ['decimal', 'float']:
                estimated_bytes_per_record += 8
            elif field.data_type in ['string', 'text']:
                avg_string_length = 50  # Estimate
                estimated_bytes_per_record += avg_string_length * 4  # UTF-8
            elif field.data_type in ['datetime', 'date']:
                estimated_bytes_per_record += 8
        
        # Add overhead for pandas DataFrame
        estimated_bytes_per_record *= 1.5
        
        # Calculate batch size to use 25% of memory limit
        available_memory = self.memory_limit_bytes * 0.25
        optimal_batch_size = int(available_memory / estimated_bytes_per_record)
        
        # Ensure reasonable bounds
        optimal_batch_size = max(1000, min(optimal_batch_size, 100000))
        
        return optimal_batch_size
    
    def _generate_batch_sync(
        self, table_schema: 'TableNode', count: int, start_idx: int
    ) -> pd.DataFrame:
        """Synchronous batch generation for multiprocessing"""
        # This would be implemented with the actual generation logic
        # Simplified for example
        from faker import Faker
        fake = Faker()
        
        data = []
        for i in range(count):
            record = {'id': start_idx + i}
            for field in table_schema.fields:
                if field.name != 'id':
                    if field.data_type == 'string':
                        record[field.name] = fake.text(max_nb_chars=50)
                    elif field.data_type == 'integer':
                        record[field.name] = fake.random_int()
                    # Add more field types as needed
            data.append(record)
        
        return pd.DataFrame(data)

# src/testdatagen/generator/batch/memory_manager.py
import psutil
import gc
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    """Monitor and manage memory usage during generation"""
    
    def __init__(self, warning_threshold: float = 0.8, critical_threshold: float = 0.9):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.process = psutil.Process()
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage statistics"""
        memory_info = self.process.memory_info()
        system_memory = psutil.virtual_memory()
        
        return {
            'process_memory_mb': memory_info.rss / (1024 * 1024),
            'process_memory_percent': self.process.memory_percent(),
            'system_memory_percent': system_memory.percent / 100,
            'available_memory_mb': system_memory.available / (1024 * 1024)
        }
    
    def check_memory_pressure(self) -> Optional[str]:
        """Check if memory usage is approaching limits"""
        usage = self.get_memory_usage()
        
        if usage['system_memory_percent'] >= self.critical_threshold:
            return "CRITICAL"
        elif usage['system_memory_percent'] >= self.warning_threshold:
            return "WARNING"
        
        return None
    
    def force_cleanup(self):
        """Force garbage collection and memory cleanup"""
        gc.collect()
        
        # Log memory usage after cleanup
        usage = self.get_memory_usage()
        logger.info(f"Memory cleanup: {usage['process_memory_mb']:.1f} MB in use")
```

### 3.3 Phase 3: Integration and Tooling (Months 7-9)

#### 3.3.1 Month 7: Database Integration

**Deliverables:**
- SQLAlchemy 2.0 integration for multiple databases
- Schema introspection capabilities
- Direct database insertion with connection pooling
- Async database operations

**Key Components:**
```python
# src/testdatagen/export/database/base.py
from abc import ABC, abstractmethod
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import MetaData, Table, Column, inspect
import pandas as pd
from typing import Dict, List, Any, Optional, AsyncGenerator
import logging

logger = logging.getLogger(__name__)

class AsyncDatabaseExporter(ABC):
    """Base class for async database exporters"""
    
    def __init__(
        self,
        connection_url: str,
        pool_size: int = 10,
        max_overflow: int = 20
    ):
        self.engine = create_async_engine(
            connection_url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=False  # Set to True for SQL debugging
        )
        self.session_factory = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self.metadata = MetaData()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.engine.dispose()
    
    async def introspect_schema(self, schema_name: Optional[str] = None) -> Dict[str, Any]:
        """Introspect database schema"""
        async with self.engine.begin() as conn:
            # Run synchronous inspection in executor
            loop = asyncio.get_event_loop()
            inspector = await loop.run_in_executor(
                None, inspect, conn.sync_connection
            )
            
            tables = await loop.run_in_executor(
                None, inspector.get_table_names, schema_name
            )
            
            schema_info = {}
            for table_name in tables:
                columns = await loop.run_in_executor(
                    None, inspector.get_columns, table_name, schema_name
                )
                schema_info[table_name] = {
                    'columns': columns,
                    'primary_keys': await loop.run_in_executor(
                        None, inspector.get_primary_keys, table_name, schema_name
                    ),
                    'foreign_keys': await loop.run_in_executor(
                        None, inspector.get_foreign_keys, table_name, schema_name
                    )
                }
            
            return schema_info
    
    async def bulk_insert_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
        batch_size: int = 10000,
        on_conflict: str = 'ignore'  # 'ignore', 'update', 'error'
    ) -> int:
        """Bulk insert DataFrame into database table"""
        total_inserted = 0
        
        # Process DataFrame in chunks for memory efficiency
        for chunk_start in range(0, len(df), batch_size):
            chunk_end = min(chunk_start + batch_size, len(df))
            chunk_df = df.iloc[chunk_start:chunk_end]
            
            records = chunk_df.to_dict('records')
            inserted_count = await self._insert_batch(table_name, records, on_conflict)
            total_inserted += inserted_count
            
            logger.info(f"Inserted batch {chunk_start//batch_size + 1}: {inserted_count} records")
        
        return total_inserted
    
    @abstractmethod
    async def _insert_batch(
        self, table_name: str, records: List[Dict], on_conflict: str
    ) -> int:
        """Insert a batch of records (implementation specific)"""
        pass

# src/testdatagen/export/database/postgres.py
from .base import AsyncDatabaseExporter
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text
from typing import List, Dict

class PostgreSQLExporter(AsyncDatabaseExporter):
    """PostgreSQL-specific database exporter"""
    
    async def _insert_batch(
        self, table_name: str, records: List[Dict], on_conflict: str
    ) -> int:
        """Insert batch with PostgreSQL-specific optimizations"""
        async with self.session_factory() as session:
            if on_conflict == 'ignore':
                # Use PostgreSQL UPSERT with ON CONFLICT DO NOTHING
                stmt = insert(table_name).values(records)
                stmt = stmt.on_conflict_do_nothing()
                result = await session.execute(stmt)
                await session.commit()
                return result.rowcount
            
            elif on_conflict == 'update':
                # Handle ON CONFLICT DO UPDATE
                stmt = insert(table_name).values(records)
                # Assume primary key is 'id' - should be configurable
                stmt = stmt.on_conflict_do_update(
                    index_elements=['id'],
                    set_={col.name: col for col in stmt.excluded if col.name != 'id'}
                )
                result = await session.execute(stmt)
                await session.commit()
                return result.rowcount
            
            else:
                # Regular insert that will fail on conflicts
                stmt = insert(table_name).values(records)
                result = await session.execute(stmt)
                await session.commit()
                return result.rowcount
    
    async def create_table_from_schema(
        self, table_name: str, schema: Dict[str, Any]
    ):
        """Create table from schema definition"""
        # Build CREATE TABLE statement
        columns_sql = []
        for field_name, field_info in schema.items():
            sql_type = self._map_type_to_sql(field_info['type'])
            nullable = "" if field_info.get('nullable', True) else "NOT NULL"
            columns_sql.append(f"{field_name} {sql_type} {nullable}")
        
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(columns_sql)}
        )
        """
        
        async with self.engine.begin() as conn:
            await conn.execute(text(create_sql))
    
    def _map_type_to_sql(self, python_type: str) -> str:
        """Map Python types to PostgreSQL types"""
        type_mapping = {
            'integer': 'INTEGER',
            'bigint': 'BIGINT',
            'string': 'VARCHAR(255)',
            'text': 'TEXT',
            'boolean': 'BOOLEAN',
            'decimal': 'DECIMAL(10,2)',
            'float': 'REAL',
            'datetime': 'TIMESTAMP',
            'date': 'DATE',
            'uuid': 'UUID'
        }
        return type_mapping.get(python_type, 'TEXT')
```

#### 3.3.2 Month 8: Language Server Protocol

**Deliverables:**
- LSP server implementation using pygls
- Syntax highlighting support
- Auto-completion for DSL constructs
- Real-time validation and error reporting
- Go-to-definition support

**Key Components:**
```python
# src/testdatagen/lsp/server.py
import asyncio
import logging
from typing import List, Optional, Dict, Any

from pygls.server import LanguageServer
from pygls.lsp.types import (
    CompletionItem, CompletionItemKind, CompletionParams,
    Diagnostic, DiagnosticSeverity, Position, Range,
    TextDocumentItem, TextDocumentContentChangeEvent,
    DidOpenTextDocumentParams, DidChangeTextDocumentParams,
    HoverParams, Hover, MarkupContent, MarkupKind
)

from ..core.parser.builder import ASTBuilder
from ..core.semantic.analyzer import SemanticAnalyzer
from .handlers.completion import CompletionHandler
from .handlers.diagnostics import DiagnosticsHandler
from .handlers.hover import HoverHandler

logger = logging.getLogger(__name__)

class TestDataGenLanguageServer(LanguageServer):
    """Language Server Protocol implementation for TestDataGen DSL"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.parser = ASTBuilder()
        self.semantic_analyzer = SemanticAnalyzer()
        
        # Handlers
        self.completion_handler = CompletionHandler()
        self.diagnostics_handler = DiagnosticsHandler()
        self.hover_handler = HoverHandler()
        
        # Document cache
        self.documents: Dict[str, str] = {}
        
        # Register LSP methods
        self._register_handlers()
    
    def _register_handlers(self):
        """Register LSP method handlers"""
        
        @self.feature('textDocument/didOpen')
        async def did_open(params: DidOpenTextDocumentParams):
            """Handle document open"""
            doc = params.text_document
            self.documents[doc.uri] = doc.text
            await self._validate_document(doc.uri, doc.text)
        
        @self.feature('textDocument/didChange')
        async def did_change(params: DidChangeTextDocumentParams):
            """Handle document changes"""
            doc_uri = params.text_document.uri
            
            # Apply changes (simplified - assumes full document sync)
            for change in params.content_changes:
                if hasattr(change, 'text'):
                    self.documents[doc_uri] = change.text
            
            await self._validate_document(doc_uri, self.documents[doc_uri])
        
        @self.feature('textDocument/completion')
        async def completion(params: CompletionParams) -> List[CompletionItem]:
            """Provide auto-completion"""
            doc_uri = params.text_document.uri
            position = params.position
            
            if doc_uri not in self.documents:
                return []
            
            document_text = self.documents[doc_uri]
            return await self.completion_handler.get_completions(
                document_text, position
            )
        
        @self.feature('textDocument/hover')
        async def hover(params: HoverParams) -> Optional[Hover]:
            """Provide hover information"""
            doc_uri = params.text_document.uri
            position = params.position
            
            if doc_uri not in self.documents:
                return None
            
            document_text = self.documents[doc_uri]
            return await self.hover_handler.get_hover_info(
                document_text, position
            )
    
    async def _validate_document(self, uri: str, text: str):
        """Validate document and send diagnostics"""
        try:
            # Parse the document
            ast = self.parser.build_ast(text)
            
            # Perform semantic analysis
            errors = self.semantic_analyzer.analyze(ast)
            
            # Convert to LSP diagnostics
            diagnostics = await self.diagnostics_handler.create_diagnostics(errors)
            
            # Send diagnostics to client
            self.publish_diagnostics(uri, diagnostics)
            
        except Exception as e:
            logger.error(f"Error validating document {uri}: {e}")
            
            # Send syntax error diagnostic
            diagnostic = Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1)
                ),
                message=f"Syntax error: {str(e)}",
                severity=DiagnosticSeverity.Error
            )
            self.publish_diagnostics(uri, [diagnostic])

# src/testdatagen/lsp/handlers/completion.py
from typing import List, Dict, Any
from pygls.lsp.types import CompletionItem, CompletionItemKind, Position
import re

class CompletionHandler:
    """Handles auto-completion for the DSL"""
    
    def __init__(self):
        # Keywords and their completion items
        self.keywords = {
            'schema': CompletionItem(
                label='schema',
                kind=CompletionItemKind.Keyword,
                detail='Schema definition',
                insert_text='schema ${1:SchemaName} {\n\t$0\n}'
            ),
            'table': CompletionItem(
                label='table',
                kind=CompletionItemKind.Keyword,
                detail='Table definition',
                insert_text='table ${1:table_name} {\n\t$0\n}'
            ),
            'generate': CompletionItem(
                label='generate',
                kind=CompletionItemKind.Keyword,
                detail='Generation block',
                insert_text='generate ${1:SchemaName} {\n\t$0\n}'
            )
        }
        
        # Data types
        self.data_types = [
            'integer', 'bigint', 'string', 'text', 'boolean',
            'decimal', 'float', 'datetime', 'date', 'uuid'
        ]
        
        # Constraint keywords
        self.constraints = [
            'min', 'max', 'length', 'pattern', 'format', 'unique',
            'not_null', 'default', 'references', 'primary_key'
        ]
        
        # Faker formats
        self.faker_formats = [
            'email', 'phone', 'name', 'address', 'company',
            'url', 'ipv4', 'credit_card', 'ssn'
        ]
    
    async def get_completions(
        self, document_text: str, position: Position
    ) -> List[CompletionItem]:
        """Get completion items for the current position"""
        
        lines = document_text.split('\n')
        if position.line >= len(lines):
            return []
        
        current_line = lines[position.line]
        prefix = current_line[:position.character]
        
        # Determine context
        context = self._get_context(lines, position.line)
        
        completions = []
        
        # Add appropriate completions based on context
        if context == 'root':
            completions.extend(self.keywords.values())
        
        elif context == 'table':
            # Inside table definition
            completions.extend([
                CompletionItem(
                    label=dt,
                    kind=CompletionItemKind.TypeParameter,
                    detail=f'{dt} data type'
                )
                for dt in self.data_types
            ])
        
        elif context == 'constraints':
            completions.extend([
                CompletionItem(
                    label=constraint,
                    kind=CompletionItemKind.Property,
                    detail=f'{constraint} constraint'
                )
                for constraint in self.constraints
            ])
        
        elif context == 'format':
            completions.extend([
                CompletionItem(
                    label=fmt,
                    kind=CompletionItemKind.Value,
                    detail=f'Faker {fmt} format'
                )
                for fmt in self.faker_formats
            ])
        
        return completions
    
    def _get_context(self, lines: List[str], current_line: int) -> str:
        """Determine the current context for completion"""
        
        # Look backwards to find the current scope
        brace_depth = 0
        for i in range(current_line, -1, -1):
            line = lines[i].strip()
            
            if '{' in line:
                brace_depth -= line.count('{')
            if '}' in line:
                brace_depth += line.count('}')
            
            if brace_depth == 0:
                if line.startswith('table'):
                    return 'table'
                elif line.startswith('schema'):
                    return 'schema'
                elif line.startswith('generate'):
                    return 'generate'
                else:
                    return 'root'
            elif brace_depth == -1:
                if 'format(' in line:
                    return 'format'
                elif any(constraint in line for constraint in self.constraints):
                    return 'constraints'
        
        return 'root'

# src/testdatagen/lsp/handlers/diagnostics.py
from typing import List, Dict, Any
from pygls.lsp.types import Diagnostic, DiagnosticSeverity, Position, Range

class DiagnosticsHandler:
    """Handles diagnostic messages (errors, warnings)"""
    
    async def create_diagnostics(self, errors: List[Dict[str, Any]]) -> List[Diagnostic]:
        """Convert semantic analysis errors to LSP diagnostics"""
        diagnostics = []
        
        for error in errors:
            severity = self._get_severity(error.get('level', 'error'))
            
            diagnostic = Diagnostic(
                range=Range(
                    start=Position(
                        line=error.get('line', 0) - 1,  # LSP is 0-based
                        character=error.get('column', 0)
                    ),
                    end=Position(
                        line=error.get('line', 0) - 1,
                        character=error.get('column', 0) + error.get('length', 1)
                    )
                ),
                message=error.get('message', 'Unknown error'),
                severity=severity,
                source='testdatagen'
            )
            diagnostics.append(diagnostic)
        
        return diagnostics
    
    def _get_severity(self, level: str) -> DiagnosticSeverity:
        """Convert error level to LSP diagnostic severity"""
        mapping = {
            'error': DiagnosticSeverity.Error,
            'warning': DiagnosticSeverity.Warning,
            'info': DiagnosticSeverity.Information,
            'hint': DiagnosticSeverity.Hint
        }
        return mapping.get(level.lower(), DiagnosticSeverity.Error)
```

#### 3.3.3 Month 9: Testing Framework Integration

**Deliverables:**
- pytest plugin for seamless integration
- unittest module support
- Django/Flask testing integration
- Custom fixture generation
- Test data lifecycle management

**Key Components:**
```python
# src/testdatagen/integrations/pytest_plugin/plugin.py
import pytest
import asyncio
from typing import Any, Dict, List, Optional, Generator
import tempfile
import os
from pathlib import Path

from ...core.parser.builder import ASTBuilder
from ...generator.engine import GenerationEngine
from ...export.formats.json_format import JSONExporter

class TestDataGenPlugin:
    """pytest plugin for TestDataGen DSL integration"""
    
    def __init__(self):
        self.parser = ASTBuilder()
        self.generator = GenerationEngine()
        self.generated_data_cache: Dict[str, Any] = {}
    
    def pytest_configure(self, config):
        """Configure pytest with TestDataGen markers"""
        config.addinivalue_line(
            "markers", "testdata(schema): mark test to use TestDataGen schema"
        )
        config.addinivalue_line(
            "markers", "seed(value): set random seed for reproducible test data"
        )

@pytest.fixture
def testdata_generator():
    """Fixture providing TestDataGen generator instance"""
    return TestDataGenPlugin()

@pytest.fixture
def tdg_schema(request):
    """Fixture for loading and parsing TestDataGen schema files"""
    marker = request.node.get_closest_marker("testdata")
    if not marker:
        pytest.skip("No testdata marker found")
    
    schema_file = marker.args[0] if marker.args else None
    if not schema_file:
        pytest.fail("testdata marker requires schema file path")
    
    # Load and parse schema
    plugin = TestDataGenPlugin()
    
    if not os.path.isabs(schema_file):
        # Resolve relative to test file
        test_file_dir = Path(request.fspath).parent
        schema_file = test_file_dir / schema_file
    
    try:
        with open(schema_file, 'r') as f:
            schema_content = f.read()
        
        ast = plugin.parser.build_ast(schema_content)
        return ast
        
    except FileNotFoundError:
        pytest.fail(f"Schema file not found: {schema_file}")
    except Exception as e:
        pytest.fail(f"Error parsing schema: {e}")

@pytest.fixture
def generate_testdata(tdg_schema, request):
    """Fixture that generates test data based on schema"""
    
    async def _generate(table_name: str, count: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """Generate test data for a specific table"""
        
        # Check for seed marker
        seed_marker = request.node.get_closest_marker("seed")
        seed = seed_marker.args[0] if seed_marker and seed_marker.args else None
        
        generator = GenerationEngine(seed=seed)
        
        # Find the table in schema
        table_node = None
        for schema in tdg_schema:
            for table in schema.tables:
                if table.name == table_name:
                    table_node = table
                    break
            if table_node:
                break
        
        if not table_node:
            raise ValueError(f"Table '{table_name}' not found in schema")
        
        # Generate data
        df = await generator.generate_table_data(table_node, count)
        return df.to_dict('records')
    
    return _generate

# Example usage in test files:
"""
# tests/test_user_service.py

@pytest.mark.testdata("../schemas/user_schema.tdg")
@pytest.mark.seed(12345)  # For reproducible tests
async def test_user_creation(generate_testdata):
    # Generate 10 users for testing
    users = await generate_testdata('users', count=10)
    
    assert len(users) == 10
    assert all('email' in user for user in users)
    assert all('@' in user['email'] for user in users)
    
    # Test your actual service
    user_service = UserService()
    for user_data in users:
        result = await user_service.create_user(user_data)
        assert result.success
"""

# src/testdatagen/integrations/pytest_plugin/fixtures.py
import pytest
from typing import Dict, Any, List
import pandas as pd
import tempfile
import json
import csv

@pytest.fixture
def testdata_to_json(generate_testdata):
    """Fixture that generates test data and saves it as JSON files"""
    json_files = []
    
    async def _save_json(table_name: str, count: int, filename: str = None) -> str:
        """Generate data and save to JSON file"""
        data = await generate_testdata(table_name, count)
        
        if filename is None:
            temp_file = tempfile.NamedTemporaryFile(
                mode='w', suffix='.json', delete=False
            )
            filename = temp_file.name
            temp_file.close()
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        json_files.append(filename)
        return filename
    
    yield _save_json
    
    # Cleanup
    import os
    for file_path in json_files:
        try:
            os.unlink(file_path)
        except OSError:
            pass

@pytest.fixture
def testdata_to_csv(generate_testdata):
    """Fixture that generates test data and saves it as CSV files"""
    csv_files = []
    
    async def _save_csv(table_name: str, count: int, filename: str = None) -> str:
        """Generate data and save to CSV file"""
        data = await generate_testdata(table_name, count)
        df = pd.DataFrame(data)
        
        if filename is None:
            temp_file = tempfile.NamedTemporaryFile(
                mode='w', suffix='.csv', delete=False
            )
            filename = temp_file.name
            temp_file.close()
        
        df.to_csv(filename, index=False)
        csv_files.append(filename)
        return filename
    
    yield _save_csv
    
    # Cleanup
    import os
    for file_path in csv_files:
        try:
            os.unlink(file_path)
        except OSError:
            pass

# src/testdatagen/integrations/django_integration/management/commands/generate_testdata.py
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import asyncio
import os

from testdatagen.core.parser.builder import ASTBuilder
from testdatagen.generator.engine import GenerationEngine
from testdatagen.export.database.base import AsyncDatabaseExporter

class Command(BaseCommand):
    """Django management command for generating test data"""
    
    help = 'Generate test data using TestDataGen DSL'
    
    def add_arguments(self, parser):
        parser.add_argument('schema_file', type=str, help='Path to TDG schema file')
        parser.add_argument('--count', type=int, default=100, help='Number of records to generate')
        parser.add_argument('--output', type=str, help='Output file (optional)')
        parser.add_argument('--format', type=str, choices=['json', 'csv', 'sql', 'database'], 
                          default='json', help='Output format')
        parser.add_argument('--seed', type=int, help='Random seed for reproducible data')
        parser.add_argument('--table', type=str, help='Generate data for specific table only')
    
    def handle(self, *args, **options):
        """Handle the command execution"""
        
        async def _async_handle():
            schema_file = options['schema_file']
            
            if not os.path.exists(schema_file):
                raise CommandError(f'Schema file does not exist: {schema_file}')
            
            # Parse schema
            parser = ASTBuilder()
            with open(schema_file, 'r') as f:
                schema_content = f.read()
            
            ast = parser.build_ast(schema_content)
            
            # Generate data
            generator = GenerationEngine(seed=options.get('seed'))
            
            if options['format'] == 'database':
                # Direct database insertion using Django settings
                from django.db import connection
                db_settings = settings.DATABASES['default']
                
                # Convert Django DB settings to SQLAlchemy URL
                db_url = self._build_db_url(db_settings)
                
                async with AsyncDatabaseExporter(db_url) as exporter:
                    for schema in ast:
                        tables_to_process = [options['table']] if options['table'] else [t.name for t in schema.tables]
                        
                        for table in schema.tables:
                            if table.name in tables_to_process:
                                self.stdout.write(f"Generating data for table: {table.name}")
                                
                                df = await generator.generate_table_data(table, options['count'])
                                await exporter.bulk_insert_dataframe(table.name, df)
                                
                                self.stdout.write(
                                    self.style.SUCCESS(f"Generated {len(df)} records for {table.name}")
                                )
            else:
                # File-based export
                for schema in ast:
                    tables_to_process = [options['table']] if options['table'] else [t.name for t in schema.tables]
                    
                    for table in schema.tables:
                        if table.name in tables_to_process:
                            self.stdout.write(f"Generating data for table: {table.name}")
                            
                            df = await generator.generate_table_data(table, options['count'])
                            
                            output_file = options['output'] or f"{table.name}_testdata.{options['format']}"
                            
                            if options['format'] == 'json':
                                df.to_json(output_file, orient='records', indent=2)
                            elif options['format'] == 'csv':
                                df.to_csv(output_file, index=False)
                            elif options['format'] == 'sql':
                                # Generate INSERT statements
                                with open(output_file, 'w') as f:
                                    for _, row in df.iterrows():
                                        values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in row.values])
                                        f.write(f"INSERT INTO {table.name} ({', '.join(df.columns)}) VALUES ({values});\n")
                            
                            self.stdout.write(
                                self.style.SUCCESS(f"Generated {len(df)} records to {output_file}")
                            )
        
        # Run async code
        asyncio.run(_async_handle())
    
    def _build_db_url(self, db_settings: Dict[str, Any]) -> str:
        """Convert Django database settings to SQLAlchemy URL"""
        engine = db_settings['ENGINE']
        
        if 'postgresql' in engine:
            driver = 'postgresql+asyncpg'
        elif 'mysql' in engine:
            driver = 'mysql+aiomysql'
        elif 'sqlite' in engine:
            return f"sqlite+aiosqlite:///{db_settings['NAME']}"
        else:
            raise CommandError(f"Unsupported database engine: {engine}")
        
        return (
            f"{driver}://{db_settings['USER']}:{db_settings['PASSWORD']}"
            f"@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}"
        )
```

### 3.4 Phase 4: Advanced Features (Months 10-12)

#### 3.4.1 Month 10: Plugin System

**Deliverables:**
- Comprehensive plugin API
- Dynamic plugin loading
- Example plugins (custom generators, exporters)
- Plugin marketplace/registry concepts

**Key Components:**
```python
# src/testdatagen/plugins/api/generator.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class PluginMetadata(BaseModel):
    """Metadata for plugin registration"""
    name: str
    version: str
    author: str
    description: str
    dependencies: List[str] = []
    entry_points: Dict[str, str] = {}

class GeneratorPlugin(ABC):
    """Base class for custom generator plugins"""
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata"""
        pass
    
    @abstractmethod
    def can_handle(self, data_type: str, constraints: Dict[str, Any]) -> bool:
        """Check if this plugin can handle the given type/constraints"""
        pass
    
    @abstractmethod
    async def generate(
        self,
        data_type: str,
        constraints: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Any:
        """Generate a value according to plugin logic"""
        pass
    
    def setup(self, config: Dict[str, Any]) -> None:
        """Setup plugin with configuration"""
        pass
    
    def teardown(self) -> None:
        """Cleanup plugin resources"""
        pass

# Example plugin implementation
class CreditCardPlugin(GeneratorPlugin):
    """Plugin for generating realistic credit card numbers"""
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="creditcard-generator",
            version="1.0.0",
            author="TestDataGen Team",
            description="Generates realistic but fake credit card numbers",
            dependencies=["python-creditcard>=1.0.0"]
        )
    
    def can_handle(self, data_type: str, constraints: Dict[str, Any]) -> bool:
        """Handle credit card format strings"""
        return (
            data_type == "string" and 
            constraints.get("format") == "credit_card"
        )
    
    async def generate(
        self,
        data_type: str,
        constraints: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Generate a fake credit card number"""
        import creditcard
        
        card_type = constraints.get("card_type", "visa")
        
        if card_type == "visa":
            return creditcard.generate_visa()
        elif card_type == "mastercard":
            return creditcard.generate_mastercard()
        elif card_type == "amex":
            return creditcard.generate_amex()
        else:
            return creditcard.generate_visa()  # Default

# src/testdatagen/plugins/loader.py
import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Type, Any
import logging

logger = logging.getLogger(__name__)

class PluginLoader:
    """Loads and manages plugins dynamically"""
    
    def __init__(self):
        self.loaded_plugins: Dict[str, Any] = {}
        self.plugin_instances: Dict[str, Any] = {}
    
    def discover_plugins(self, plugin_dir: Path) -> List[str]:
        """Discover available plugins in directory"""
        discovered = []
        
        if not plugin_dir.exists():
            return discovered
        
        for plugin_file in plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
                
            discovered.append(plugin_file.stem)
        
        return discovered
    
    def load_plugin(self, plugin_path: Path, plugin_name: str) -> bool:
        """Load a single plugin"""
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None:
                logger.error(f"Could not load spec for plugin: {plugin_path}")
                return False
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)
            
            # Look for plugin classes
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    hasattr(attr, 'metadata') and 
                    attr != GeneratorPlugin):  # Not the base class
                    
                    plugin_instance = attr()
                    self.plugin_instances[plugin_instance.metadata.name] = plugin_instance
                    logger.info(f"Loaded plugin: {plugin_instance.metadata.name}")
                    
                    return True
            
            logger.warning(f"No valid plugin class found in {plugin_path}")
            return False
            
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_path}: {e}")
            return False
    
    def get_plugin(self, plugin_name: str) -> Optional[Any]:
        """Get a loaded plugin instance"""
        return self.plugin_instances.get(plugin_name)
    
    def get_plugins_for_type(self, data_type: str, constraints: Dict[str, Any]) -> List[Any]:
        """Get all plugins that can handle the given type/constraints"""
        matching_plugins = []
        
        for plugin in self.plugin_instances.values():
            if plugin.can_handle(data_type, constraints):
                matching_plugins.append(plugin)
        
        return matching_plugins

# src/testdatagen/plugins/registry.py
from typing import Dict, List, Optional
import aiohttp
import asyncio
from pathlib import Path
import json

class PluginRegistry:
    """Registry for discovering and installing plugins"""
    
    def __init__(self, registry_url: str = "https://plugins.testdatagen.dev"):
        self.registry_url = registry_url
        self.local_plugins_dir = Path.home() / ".testdatagen" / "plugins"
        self.local_plugins_dir.mkdir(parents=True, exist_ok=True)
    
    async def search_plugins(self, query: str) -> List[Dict[str, Any]]:
        """Search for plugins in the registry"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.registry_url}/search",
                params={"q": query}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return []
    
    async def install_plugin(self, plugin_name: str, version: str = "latest") -> bool:
        """Install a plugin from the registry"""
        try:
            # Download plugin metadata
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.registry_url}/plugins/{plugin_name}/{version}"
                ) as response:
                    if response.status != 200:
                        return False
                    
                    plugin_info = await response.json()
                
                # Download plugin code
                async with session.get(plugin_info["download_url"]) as response:
                    if response.status != 200:
                        return False
                    
                    plugin_code = await response.text()
                
                # Save plugin locally
                plugin_file = self.local_plugins_dir / f"{plugin_name}.py"
                with open(plugin_file, 'w') as f:
                    f.write(plugin_code)
                
                # Save metadata
                metadata_file = self.local_plugins_dir / f"{plugin_name}.json"
                with open(metadata_file, 'w') as f:
                    json.dump(plugin_info, f, indent=2)
                
                return True
                
        except Exception as e:
            logger.error(f"Error installing plugin {plugin_name}: {e}")
            return False
    
    def list_installed_plugins(self) -> List[Dict[str, Any]]:
        """List locally installed plugins"""
        installed = []
        
        for metadata_file in self.local_plugins_dir.glob("*.json"):
            try:
                with open(metadata_file) as f:
                    plugin_info = json.load(f)
                    installed.append(plugin_info)
            except Exception:
                continue
        
        return installed
```

#### 3.4.2 Month 11: Enterprise Features

**Deliverables:**
- Advanced data masking and privacy features
- Audit logging and compliance
- Configuration management
- Role-based access control
- Performance monitoring and analytics

**Key Components:**
```python
# src/testdatagen/enterprise/privacy/masking.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import hashlib
import hmac
from cryptography.fernet import Fernet
import re

class DataMaskingStrategy(ABC):
    """Base class for data masking strategies"""
    
    @abstractmethod
    def mask(self, value: Any, context: Dict[str, Any]) -> Any:
        """Mask the given value"""
        pass

class EmailMaskingStrategy(DataMaskingStrategy):
    """Mask email addresses while preserving format"""
    
    def mask(self, value: str, context: Dict[str, Any]) -> str:
        if '@' not in value:
            return value
        
        local, domain = value.split('@', 1)
        
        # Keep first and last character, mask middle
        if len(local) <= 2:
            masked_local = '*' * len(local)
        else:
            masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
        
        return f"{masked_local}@{domain}"

class CreditCardMaskingStrategy(DataMaskingStrategy):
    """Mask credit card numbers showing only last 4 digits"""
    
    def mask(self, value: str, context: Dict[str, Any]) -> str:
        # Remove spaces and hyphens
        clean_value = re.sub(r'[\s\-]', '', value)
        
        if len(clean_value) < 4:
            return '*' * len(clean_value)
        
        return '*' * (len(clean_value) - 4) + clean_value[-4:]

class FormatPreservingEncryption(DataMaskingStrategy):
    """Format-preserving encryption for sensitive data"""
    
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def mask(self, value: str, context: Dict[str, Any]) -> str:
        # Simple FPE implementation (production would use proper FPE library)
        encrypted = self.cipher.encrypt(value.encode())
        # Convert to format-preserving output
        return self._preserve_format(value, encrypted.hex())
    
    def _preserve_format(self, original: str, encrypted_hex: str) -> str:
        """Preserve the format of the original string"""
        result = []
        hex_index = 0
        
        for char in original:
            if hex_index >= len(encrypted_hex):
                hex_index = 0
            
            if char.isdigit():
                # Map hex to digit
                hex_val = int(encrypted_hex[hex_index], 16)
                result.append(str(hex_val % 10))
            elif char.isalpha():
                # Map hex to letter
                hex_val = int(encrypted_hex[hex_index], 16)
                if char.isupper():
                    result.append(chr(ord('A') + (hex_val % 26)))
                else:
                    result.append(chr(ord('a') + (hex_val % 26)))
            else:
                # Preserve special characters
                result.append(char)
            
            hex_index += 1
        
        return ''.join(result)

# src/testdatagen/enterprise/audit/logger.py
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import asyncio
import aiofiles

class AuditLogger:
    """Comprehensive audit logging for enterprise compliance"""
    
    def __init__(
        self,
        log_file: Path,
        log_level: str = "INFO",
        include_data_samples: bool = False
    ):
        self.log_file = log_file
        self.include_data_samples = include_data_samples
        
        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup structured logging
        self.logger = logging.getLogger("testdatagen.audit")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # JSON formatter for structured logs
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    async def log_generation_start(
        self,
        schema_name: str,
        table_name: str,
        record_count: int,
        user_id: Optional[str] = None
    ):
        """Log the start of data generation"""
        await self._log_event("generation_start", {
            "schema_name": schema_name,
            "table_name": table_name,
            "record_count": record_count,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def log_generation_complete(
        self,
        schema_name: str,
        table_name: str,
        records_generated: int,
        duration_seconds: float,
        output_format: str,
        data_sample: Optional[Dict[str, Any]] = None
    ):
        """Log successful completion of data generation"""
        event_data = {
            "schema_name": schema_name,
            "table_name": table_name,
            "records_generated": records_generated,
            "duration_seconds": duration_seconds,
            "output_format": output_format,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if self.include_data_samples and data_sample:
            event_data["data_sample"] = data_sample
        
        await self._log_event("generation_complete", event_data)
    
    async def log_data_access(
        self,
        table_name: str,
        access_type: str,  # "read", "export", "delete"
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Log data access events"""
        await self._log_event("data_access", {
            "table_name": table_name,
            "access_type": access_type,
            "user_id": user_id,
            "ip_address": ip_address,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def log_error(
        self,
        error_type: str,
        error_message: str,
        context: Dict[str, Any],
        user_id: Optional[str] = None
    ):
        """Log error events"""
        await self._log_event("error", {
            "error_type": error_type,
            "error_message": error_message,
            "context": context,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def _log_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log a structured event"""
        log_entry = {
            "event_type": event_type,
            "data": event_data
        }
        
        # Write asynchronously to avoid blocking generation
        async with aiofiles.open(self.log_file, 'a') as f:
            await f.write(json.dumps(log_entry) + '\n')

# src/testdatagen/enterprise/config/manager.py
from typing import Dict, Any, Optional, List
from pathlib import Path
import yaml
import json
from pydantic import BaseModel, Field
import os

class DatabaseConfig(BaseModel):
    """Database connection configuration"""
    driver: str
    host: str
    port: int
    username: str
    password: str = Field(exclude=True)  # Exclude from serialization
    database: str
    ssl_mode: str = "prefer"
    pool_size: int = 10
    max_overflow: int = 20

class SecurityConfig(BaseModel):
    """Security and privacy configuration"""
    enable_audit_logging: bool = True
    audit_log_path: Path = Field(default_factory=lambda: Path("/var/log/testdatagen/audit.log"))
    enable_data_masking: bool = False
    masking_key: Optional[str] = None
    allowed_export_formats: List[str] = Field(default_factory=lambda: ["json", "csv"])
    max_records_per_request: int = 100000

class PerformanceConfig(BaseModel):
    """Performance tuning configuration"""
    max_workers: int = Field(default_factory=lambda: os.cpu_count() or 4)
    batch_size: int = 10000
    memory_limit_gb: float = 2.0
    enable_parallel_generation: bool = True
    cache_generated_data: bool = True
    cache_size_mb: int = 512

class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".testdatagen" / "config.yaml"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        if self.config_path.exists():
            with open(self.config_path) as f:
                if self.config_path.suffix.lower() == '.yaml':
                    self._config = yaml.safe_load(f) or {}
                else:
                    self._config = json.load(f) or {}
        else:
            self._config = self._get_default_config()
            self.save_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "databases": {},
            "security": SecurityConfig().dict(),
            "performance": PerformanceConfig().dict(),
            "plugins": {
                "enabled": [],
                "directories": []
            }
        }
    
    def get_database_config(self, name: str) -> Optional[DatabaseConfig]:
        """Get database configuration by name"""
        db_config = self._config.get("databases", {}).get(name)
        if db_config:
            return DatabaseConfig(**db_config)
        return None
    
    def set_database_config(self, name: str, config: DatabaseConfig):
        """Set database configuration"""
        if "databases" not in self._config:
            self._config["databases"] = {}
        self._config["databases"][name] = config.dict()
        self.save_config()
    
    def get_security_config(self) -> SecurityConfig:
        """Get security configuration"""
        return SecurityConfig(**self._config.get("security", {}))
    
    def get_performance_config(self) -> PerformanceConfig:
        """Get performance configuration"""
        return PerformanceConfig(**self._config.get("performance", {}))
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            if self.config_path.suffix.lower() == '.yaml':
                yaml.dump(self._config, f, default_flow_style=False, indent=2)
            else:
                json.dump(self._config, f, indent=2)

# src/testdatagen/enterprise/monitoring/metrics.py
import time
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import psutil
from collections import defaultdict, deque

@dataclass
class GenerationMetrics:
    """Metrics for a single generation operation"""
    table_name: str
    start_time: float
    end_time: Optional[float] = None
    records_generated: int = 0
    memory_peak_mb: float = 0
    cpu_percent: float = 0
    errors: List[str] = field(default_factory=list)
    
    @property
    def duration_seconds(self) -> Optional[float]:
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    @property
    def records_per_second(self) -> Optional[float]:
        if self.duration_seconds and self.duration_seconds > 0:
            return self.records_generated / self.duration_seconds
        return None

class PerformanceMonitor:
    """Monitor performance metrics during generation"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.current_operations: Dict[str, GenerationMetrics] = {}
        self.completed_operations: deque = deque(maxlen=max_history)
        self.system_metrics_history: deque = deque(maxlen=max_history)
        self.process = psutil.Process()
        
        # Start background monitoring
        self._monitoring_task = None
        self._monitoring_active = False
    
    async def start_monitoring(self):
        """Start background system monitoring"""
        if not self._monitoring_active:
            self._monitoring_active = True
            self._monitoring_task = asyncio.create_task(self._monitor_system())
    
    async def stop_monitoring(self):
        """Stop background monitoring"""
        self._monitoring_active = False
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
    
    def start_generation(self, operation_id: str, table_name: str) -> GenerationMetrics:
        """Start monitoring a generation operation"""
        metrics = GenerationMetrics(
            table_name=table_name,
            start_time=time.time()
        )
        self.current_operations[operation_id] = metrics
        return metrics
    
    def update_generation(
        self,
        operation_id: str,
        records_generated: int,
        memory_mb: Optional[float] = None
    ):
        """Update metrics for ongoing generation"""
        if operation_id in self.current_operations:
            metrics = self.current_operations[operation_id]
            metrics.records_generated = records_generated
            
            if memory_mb:
                metrics.memory_peak_mb = max(metrics.memory_peak_mb, memory_mb)
    
    def finish_generation(self, operation_id: str, success: bool = True, error: str = None):
        """Finish monitoring a generation operation"""
        if operation_id in self.current_operations:
            metrics = self.current_operations.pop(operation_id)
            metrics.end_time = time.time()
            
            if not success and error:
                metrics.errors.append(error)
            
            self.completed_operations.append(metrics)
    
    async def _monitor_system(self):
        """Background system monitoring"""
        while self._monitoring_active:
            try:
                # Collect system metrics
                memory_info = self.process.memory_info()
                cpu_percent = self.process.cpu_percent()
                system_memory = psutil.virtual_memory()
                
                system_metrics = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "process_memory_mb": memory_info.rss / (1024 * 1024),
                    "process_cpu_percent": cpu_percent,
                    "system_memory_percent": system_memory.percent,
                    "system_cpu_percent": psutil.cpu_percent(),
                    "active_operations": len(self.current_operations)
                }
                
                self.system_metrics_history.append(system_metrics)
                
                # Update current operations with CPU info
                for metrics in self.current_operations.values():
                    metrics.cpu_percent = cpu_percent
                
                await asyncio.sleep(1)  # Sample every second
                
            except Exception as e:
                # Don't let monitoring errors crash the application
                continue
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics"""
        if not self.completed_operations:
            return {"message": "No completed operations to analyze"}
        
        # Calculate statistics
        durations = [op.duration_seconds for op in self.completed_operations if op.duration_seconds]
        record_rates = [op.records_per_second for op in self.completed_operations if op.records_per_second]
        memory_peaks = [op.memory_peak_mb for op in self.completed_operations]
        
        total_records = sum(op.records_generated for op in self.completed_operations)
        total_errors = sum(len(op.errors) for op in self.completed_operations)
        
        return {
            "total_operations": len(self.completed_operations),
            "total_records_generated": total_records,
            "total_errors": total_errors,
            "average_duration_seconds": sum(durations) / len(durations) if durations else 0,
            "average_records_per_second": sum(record_rates) / len(record_rates) if record_rates else 0,
            "peak_memory_mb": max(memory_peaks) if memory_peaks else 0,
            "average_memory_mb": sum(memory_peaks) / len(memory_peaks) if memory_peaks else 0,
            "success_rate": (len(self.completed_operations) - total_errors) / len(self.completed_operations)
        }
```

#### 3.4.3 Month 12: Production Readiness and Documentation

**Deliverables:**
- Comprehensive documentation with Sphinx
- Production deployment guides
- Performance tuning recommendations
- Security hardening guidelines
- Migration tools and upgrade paths

**Key Components:**
```python
# src/testdatagen/cli/commands/server.py
import asyncio
from typing import Optional
import uvicorn
import click
from rich.console import Console
from rich.table import Table

from ...web.app import create_app
from ...enterprise.config.manager import ConfigManager

console = Console()

@click.command()
@click.option('--host', default='127.0.0.1', help='Host to bind the server to')
@click.option('--port', default=8000, type=int, help='Port to bind the server to')
@click.option('--workers', default=1, type=int, help='Number of worker processes')
@click.option('--reload', is_flag=True, help='Enable auto-reload for development')
@click.option('--config-file', type=click.Path(exists=True), help='Configuration file path')
def server(host: str, port: int, workers: int, reload: bool, config_file: Optional[str]):
    """Start the TestDataGen web server"""
    
    console.print("[bold green]Starting TestDataGen Server[/bold green]")
    
    # Load configuration
    config_manager = ConfigManager()
    if config_file:
        config_manager.config_path = Path(config_file)
    
    # Display server info
    table = Table(title="Server Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Host", host)
    table.add_row("Port", str(port))
    table.add_row("Workers", str(workers))
    table.add_row("Reload", str(reload))
    table.add_row("Config File", str(config_manager.config_path))
    
    console.print(table)
    
    # Create FastAPI app
    app = create_app(config_manager)
    
    # Run server
    uvicorn.run(
        app,
        host=host,
        port=port,
        workers=workers,
        reload=reload,
        access_log=True
    )

# src/testdatagen/web/app.py
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging

from .routers import generation, validation, schema
from ..enterprise.config.manager import ConfigManager
from ..enterprise.audit.logger import AuditLogger
from ..enterprise.monitoring.metrics import PerformanceMonitor

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting TestDataGen API server")
    
    # Start performance monitoring
    monitor = app.state.performance_monitor
    await monitor.start_monitoring()
    
    yield
    
    # Shutdown
    logger.info("Shutting down TestDataGen API server")
    await monitor.stop_monitoring()

def create_app(config_manager: ConfigManager) -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="TestDataGen API",
        description="REST API for TestDataGen DSL",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Application state
    app.state.config_manager = config_manager
    app.state.audit_logger = AuditLogger(
        config_manager.get_security_config().audit_log_path
    )
    app.state.performance_monitor = PerformanceMonitor()
    
    # Include routers
    app.include_router(generation.router, prefix="/api/v1/generation", tags=["generation"])
    app.include_router(validation.router, prefix="/api/v1/validation", tags=["validation"])
    app.include_router(schema.router, prefix="/api/v1/schema", tags=["schema"])
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "version": "1.0.0"}
    
    @app.get("/metrics")
    async def metrics():
        """Performance metrics endpoint"""
        monitor = app.state.performance_monitor
        return monitor.get_performance_summary()
    
    return app

# tools/benchmark.py
import asyncio
import time
from pathlib import Path
import pandas as pd
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.testdatagen.core.parser.builder import ASTBuilder
from src.testdatagen.generator.engine import GenerationEngine

console = Console()

@click.command()
@click.option('--schema-file', required=True, type=click.Path(exists=True), help='Schema file to benchmark')
@click.option('--record-counts', default='1000,10000,100000', help='Comma-separated list of record counts to test')
@click.option('--iterations', default=3, type=int, help='Number of iterations per test')
@click.option('--output', type=click.Path(), help='Output file for results')
def benchmark(schema_file: str, record_counts: str, iterations: int, output: str):
    """Benchmark TestDataGen performance"""
    
    console.print("[bold blue]TestDataGen Performance Benchmark[/bold blue]")
    
    # Parse record counts
    counts = [int(c.strip()) for c in record_counts.split(',')]
    
    # Load schema
    parser = ASTBuilder()
    with open(schema_file) as f:
        schema_content = f.read()
    
    ast = parser.build_ast(schema_content)
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        for record_count in counts:
            for iteration in range(iterations):
                task = progress.add_task(
                    f"Testing {record_count:,} records (iteration {iteration + 1})",
                    total=None
                )
                
                # Run benchmark
                result = asyncio.run(run_benchmark(ast, record_count))
                result['iteration'] = iteration + 1
                results.append(result)
                
                progress.remove_task(task)
    
    # Calculate averages
    df = pd.DataFrame(results)
    summary = df.groupby(['table_name', 'record_count']).agg({
        'duration_seconds': ['mean', 'std'],
        'records_per_second': ['mean', 'std'],
        'memory_mb': ['mean', 'max'],
    }).round(2)
    
    # Display results
    console.print("\n[bold green]Benchmark Results[/bold green]")
    
    table = Table()
    table.add_column("Table")
    table.add_column("Records")
    table.add_column("Avg Duration (s)")
    table.add_column("Avg Rate (rec/s)")
    table.add_column("Peak Memory (MB)")
    
    for (table_name, record_count), row in summary.iterrows():
        table.add_row(
            table_name,
            f"{record_count:,}",
            f"{row[('duration_seconds', 'mean')]:.2f} ± {row[('duration_seconds', 'std')]:.2f}",
            f"{row[('records_per_second', 'mean')]:,.0f} ± {row[('records_per_second', 'std')]:,.0f}",
            f"{row[('memory_mb', 'max')]:,.1f}"
        )
    
    console.print(table)
    
    # Save results
    if output:
        df.to_csv(output, index=False)
        console.print(f"\n[green]Results saved to {output}[/green]")

async def run_benchmark(ast, record_count: int) -> dict:
    """Run a single benchmark test"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / (1024 * 1024)
    
    generator = GenerationEngine(seed=42)  # Fixed seed for reproducibility
    
    results = []
    for schema in ast:
        for table in schema.tables:
            start_time = time.time()
            
            df = await generator.generate_table_data(table, record_count)
            
            end_time = time.time()
            memory_after = process.memory_info().rss / (1024 * 1024)
            
            duration = end_time - start_time
            records_per_second = record_count / duration if duration > 0 else 0
            
            results.append({
                'table_name': table.name,
                'record_count': record_count,
                'duration_seconds': duration,
                'records_per_second': records_per_second,
                'memory_mb': memory_after - memory_before,
                'records_generated': len(df)
            })
    
    return results[0] if results else {}

if __name__ == '__main__':
    benchmark()

# Setup comprehensive development tooling
# requirements-dev.txt
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0
pytest-benchmark>=4.0.0
hypothesis>=6.88.0

black>=23.9.0
ruff>=0.1.0
mypy>=1.6.0
pre-commit>=3.5.0

sphinx>=7.2.0
sphinx-rtd-theme>=1.3.0
sphinx-autodoc-typehints>=1.24.0
myst-parser>=2.0.0

ipython>=8.16.0
jupyter>=1.0.0
notebook>=7.0.0

# Performance profiling
py-spy>=0.3.14
memory-profiler>=0.61.0
line-profiler>=4.1.0

# Database testing
pytest-postgresql>=5.0.0
pytest-mysql>=2.3.0
```

## 4. CI/CD Pipeline and Deployment

### 4.1 GitHub Actions Workflows

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.11', '3.12']
        
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpassword
          POSTGRES_USER: testuser
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install Java (for ANTLR)
      uses: actions/setup-java@v3
      with:
        distribution: 'temurin'
        java-version: '17'
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
        
    - name: Generate ANTLR parsers
      run: |
        python tools/generate_antlr.py
        
    - name: Lint with ruff
      run: ruff check src tests
    
    - name: Format check with black
      run: black --check src tests
    
    - name: Type check with mypy
      run: mypy src
    
    - name: Run tests
      run: |
        pytest tests/ \
          --cov=src/testdatagen \
          --cov-report=xml \
          --cov-report=html \
          --junit-xml=test-results.xml
      env:
        DATABASE_URL: postgresql://testuser:testpassword@localhost:5432/testdb
    
    - name: Run benchmarks
      if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
      run: |
        python tools/benchmark.py \
          --schema-file examples/basic/simple_table.tdg \
          --record-counts "1000,10000" \
          --iterations 2 \
          --output benchmark-results.csv
    
    - name: Upload coverage to Codecov
      if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results-${{ matrix.os }}-py${{ matrix.python-version }}
        path: |
          test-results.xml
          htmlcov/
          benchmark-results.csv

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run security scan
      uses: pypa/gh-action-pip-audit@v1.0.8
      with:
        inputs: requirements.txt requirements-dev.txt
        
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
        
    - name: Build documentation
      run: |
        cd docs
        make html
        
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/_build/html

  release:
    needs: [test, security, docs]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
        
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install build tools
      run: |
        pip install build twine
        
    - name: Build package
      run: |
        python -m build
        
    - name: Publish to PyPI
      if: startsWith(github.ref, 'refs/tags/v')
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        twine upload dist/*
```

## 5. Success Metrics and Timeline

### 5.1 Key Performance Indicators
- **Generation Speed**: 50,000+ records/second for simple schemas
- **Memory Efficiency**: <1GB for generating 1M records
- **Test Coverage**: >95% code coverage
- **Documentation Coverage**: 100% API documentation
- **User Adoption**: 1,000+ PyPI downloads in first 6 months

### 5.2 Quality Gates
- All CI/CD checks passing
- Security vulnerability scan clean
- Performance benchmarks within targets
- User acceptance testing completed

This Python-based implementation plan leverages the rich Python ecosystem while maintaining the sophisticated DSL capabilities outlined in the requirements. The choice of mature libraries like SQLAlchemy, pandas, and FastAPI ensures enterprise-grade reliability while the ANTLR4 parser provides robust language processing capabilities.