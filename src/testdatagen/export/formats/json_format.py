





























import os
from typing import Dict, List, Optional, Any, Union
import pandas as pd
import json

from ..base import Exporter


class JsonExporter(Exporter):
    """Exporter for JSON format"""
    
    def export(self, data: pd.DataFrame, output_path: str, **options) -> None:
        """
        Export data to a JSON file
        
        Args:
            data: The data to export
            output_path: The path to write the output to
            **options: Additional options for the exporter
                - orient: The format of the JSON string, default 'records'
                - indent: The indentation level, default 2
                - date_format: The format for dates, default 'iso'
        """
        # Get options
        orient = options.get("orient", "records")
        indent = options.get("indent", 2)
        date_format = options.get("date_format", "iso")
        
        # Convert to JSON
        json_data = data.to_json(
            orient=orient,
            date_format=date_format,
            indent=indent
        )
        
        # Write to file
        with open(output_path, "w") as f:
            f.write(json_data)
    
    def export_all(self, data: Dict[str, pd.DataFrame], output_dir: str, **options) -> Dict[str, str]:
        """
        Export multiple datasets to JSON files
        
        Args:
            data: A dictionary of table names to DataFrames
            output_dir: The directory to write the output to
            **options: Additional options for the exporter
                - file_suffix: The suffix to add to file names, default '.json'
                - orient: The format of the JSON string, default 'records'
                - indent: The indentation level, default 2
                - date_format: The format for dates, default 'iso'
            
        Returns:
            A dictionary of table names to output file paths
        """
        # Get options
        file_suffix = options.get("file_suffix", ".json")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Export each dataset
        result = {}
        for table_name, df in data.items():
            output_path = os.path.join(output_dir, f"{table_name}{file_suffix}")
            self.export(df, output_path, **options)
            result[table_name] = output_path
        
        return result





























