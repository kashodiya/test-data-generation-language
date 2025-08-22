



























from typing import Dict, List, Optional, Any, Union
from abc import ABC, abstractmethod
import pandas as pd


class Exporter(ABC):
    """Base class for data exporters"""
    
    @abstractmethod
    def export(self, data: pd.DataFrame, output_path: str, **options) -> None:
        """
        Export data to a file
        
        Args:
            data: The data to export
            output_path: The path to write the output to
            **options: Additional options for the exporter
        """
        pass
    
    @abstractmethod
    def export_all(self, data: Dict[str, pd.DataFrame], output_dir: str, **options) -> Dict[str, str]:
        """
        Export multiple datasets to files
        
        Args:
            data: A dictionary of table names to DataFrames
            output_dir: The directory to write the output to
            **options: Additional options for the exporter
            
        Returns:
            A dictionary of table names to output file paths
        """
        pass



























