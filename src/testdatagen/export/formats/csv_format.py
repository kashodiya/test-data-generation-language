































import os
from typing import Dict, List, Optional, Any, Union
import pandas as pd

from ..base import Exporter


class CsvExporter(Exporter):
    """Exporter for CSV format"""
    
    def export(self, data: pd.DataFrame, output_path: str, **options) -> None:
        """
        Export data to a CSV file
        
        Args:
            data: The data to export
            output_path: The path to write the output to
            **options: Additional options for the exporter
                - sep: The separator to use, default ','
                - index: Whether to include the index, default False
                - header: Whether to include the header, default True
                - encoding: The encoding to use, default 'utf-8'
                - date_format: The format for dates, default None
        """
        # Get options
        sep = options.get("sep", ",")
        index = options.get("index", False)
        header = options.get("header", True)
        encoding = options.get("encoding", "utf-8")
        date_format = options.get("date_format", None)
        
        # Export to CSV
        data.to_csv(
            output_path,
            sep=sep,
            index=index,
            header=header,
            encoding=encoding,
            date_format=date_format
        )
    
    def export_all(self, data: Dict[str, pd.DataFrame], output_dir: str, **options) -> Dict[str, str]:
        """
        Export multiple datasets to CSV files
        
        Args:
            data: A dictionary of table names to DataFrames
            output_dir: The directory to write the output to
            **options: Additional options for the exporter
                - file_suffix: The suffix to add to file names, default '.csv'
                - sep: The separator to use, default ','
                - index: Whether to include the index, default False
                - header: Whether to include the header, default True
                - encoding: The encoding to use, default 'utf-8'
                - date_format: The format for dates, default None
            
        Returns:
            A dictionary of table names to output file paths
        """
        # Get options
        file_suffix = options.get("file_suffix", ".csv")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Export each dataset
        result = {}
        for table_name, df in data.items():
            output_path = os.path.join(output_dir, f"{table_name}{file_suffix}")
            self.export(df, output_path, **options)
            result[table_name] = output_path
        
        return result































