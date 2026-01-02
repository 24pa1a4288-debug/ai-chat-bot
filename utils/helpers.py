"""
Helper utility functions
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional


def save_data(data: Dict, filename: str, directory: str = "data"):
    """
    Save data to JSON file
    
    Args:
        data: Data dictionary to save
        filename: Name of the file
        directory: Directory to save in
    """
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def load_data(filename: str, directory: str = "data") -> Optional[Dict]:
    """
    Load data from JSON file
    
    Args:
        filename: Name of the file
        directory: Directory to load from
        
    Returns:
        Loaded data dictionary or None
    """
    filepath = os.path.join(directory, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime to readable string
    
    Args:
        dt: Datetime object
        
    Returns:
        Formatted string
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def create_report_file(report_content: str, filename: Optional[str] = None) -> str:
    """
    Create a report file
    
    Args:
        report_content: Content of the report
        filename: Optional filename (auto-generated if not provided)
        
    Returns:
        Path to created file
    """
    os.makedirs("reports", exist_ok=True)
    
    if filename is None:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    filepath = os.path.join("reports", filename)
    
    with open(filepath, 'w') as f:
        f.write(report_content)
    
    return filepath

