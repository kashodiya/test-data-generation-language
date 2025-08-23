

























import sys
import os
import click
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel
import pandas as pd

from ..core.parser import Parser
from ..core.semantic.validator import Validator
from ..generator.engine import GenerationEngine, GenerationOptions
from ..generator.strategies.random_strategy import RandomStrategy
from ..generator.strategies.faker_strategy import FakerStrategy
from ..export.formats.json_format import JsonExporter
from ..export.formats.csv_format import CsvExporter


console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """TestDataGen - A DSL for generating test data"""
    pass


@main.command()
@click.argument("schema_file", type=click.Path(exists=True, readable=True))
@click.option("--validate-only", is_flag=True, help="Only validate the schema, don't generate data")
def validate(schema_file, validate_only):
    """Validate a schema file"""
    console.print(f"Validating schema file: [bold]{schema_file}[/bold]")
    
    # Parse the schema
    parser = Parser()
    result = parser.parse_file(schema_file)
    
    if not result.success:
        console.print("[bold red]Parsing failed![/bold red]")
        for error in result.errors:
            console.print(f"[red]Error at line {error.line}, column {error.column}: {error.message}[/red]")
        sys.exit(1)
    
    # Validate the schema
    validator = Validator()
    errors = validator.validate(result.ast)
    
    if errors:
        console.print("[bold yellow]Validation found issues:[/bold yellow]")
        for error in errors:
            color = "red" if error.severity == "error" else "yellow"
            console.print(f"[{color}]{error.severity.upper()} at line {error.line}, column {error.column}: {error.message}[/{color}]")
        
        # Exit if there are errors
        if any(error.severity == "error" for error in errors):
            console.print("[bold red]Validation failed with errors![/bold red]")
            sys.exit(1)
        else:
            console.print("[bold yellow]Validation completed with warnings.[/bold yellow]")
    else:
        console.print("[bold green]Validation successful![/bold green]")
    
    # Display schema summary
    schema = result.ast
    console.print(f"\nSchema: [bold]{schema.name}[/bold]")
    
    summary_table = Table(title="Tables")
    summary_table.add_column("Table Name", style="cyan")
    summary_table.add_column("Fields", style="green")
    summary_table.add_column("Constraints", style="yellow")
    
    for table_node in schema.tables:
        summary_table.add_row(
            table_node.name,
            str(len(table_node.fields)),
            str(len(table_node.constraints))
        )
    
    console.print(summary_table)


@main.command()
@click.argument("schema_file", type=click.Path(exists=True, readable=True))
@click.option("--count", "-c", default=100, help="Number of records to generate")
@click.option("--output", "-o", default="output", help="Output directory")
@click.option("--format", "-f", type=click.Choice(["json", "csv"]), default="json", help="Output format")
@click.option("--strategy", "-s", type=click.Choice(["random", "faker"]), default="faker", help="Generation strategy")
@click.option("--seed", type=int, help="Random seed for reproducible generation")
@click.option("--locale", default="en_US", help="Locale for Faker strategy")
def generate(schema_file, count, output, format, strategy, seed, locale):
    """Generate test data from a schema file"""
    console.print(f"Generating test data from schema: [bold]{schema_file}[/bold]")
    
    # Parse the schema
    parser = Parser()
    result = parser.parse_file(schema_file)
    
    if not result.success:
        console.print("[bold red]Parsing failed![/bold red]")
        for error in result.errors:
            console.print(f"[red]Error at line {error.line}, column {error.column}: {error.message}[/red]")
        sys.exit(1)
    
    # Validate the schema
    validator = Validator()
    errors = validator.validate(result.ast)
    
    if errors and any(error.severity == "error" for error in errors):
        console.print("[bold red]Validation failed![/bold red]")
        for error in errors:
            if error.severity == "error":
                console.print(f"[red]Error at line {error.line}, column {error.column}: {error.message}[/red]")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output):
        os.makedirs(output)
    
    # Initialize generation engine
    strategies = {
        "random": RandomStrategy(),
        "faker": FakerStrategy()
    }
    
    engine = GenerationEngine(strategies)
    
    # Set up generation options
    options = GenerationOptions(
        record_count=count,
        seed=seed,
        locale=locale,
        strategy=strategy
    )
    
    # Generate data
    console.print(f"Generating [bold]{count}[/bold] records using [bold]{strategy}[/bold] strategy...")
    result = engine.generate(result.ast, options)
    
    if not result.success:
        console.print("[bold red]Generation failed![/bold red]")
        for error in result.errors:
            console.print(f"[red]Error: {error}[/red]")
        sys.exit(1)
    
    # Export data
    console.print(f"Exporting data to [bold]{format}[/bold] format...")
    
    if format == "json":
        exporter = JsonExporter()
    else:  # csv
        exporter = CsvExporter()
    
    for table_name, df in result.data.items():
        file_path = os.path.join(output, f"{table_name}.{format}")
        exporter.export(df, file_path)
        console.print(f"Exported [bold]{len(df)}[/bold] records to [bold]{file_path}[/bold]")
    
    # Print statistics
    console.print("\n[bold]Generation Statistics:[/bold]")
    console.print(f"Total records: [bold]{result.stats['total_records']}[/bold]")
    console.print(f"Total time: [bold]{result.stats['generation_time_ms']:.2f}ms[/bold]")
    
    console.print("[bold green]Generation completed successfully![/bold green]")


@main.command()
@click.argument("schema_file", type=click.Path(exists=True, readable=True))
def show(schema_file):
    """Display a schema file with syntax highlighting"""
    with open(schema_file, "r") as f:
        content = f.read()
    
    syntax = Syntax(content, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=schema_file, expand=False))


if __name__ == "__main__":
    main()

























