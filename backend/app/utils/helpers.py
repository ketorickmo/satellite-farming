import traceback
from datetime import datetime

def format_exception(exception):
    """
    Format an exception for logging
    
    Args:
        exception: The exception to format
        
    Returns:
        str: Formatted exception message
    """
    return f"{type(exception).__name__}: {str(exception)}"

def format_datetime(dt):
    """
    Format a datetime object for API responses
    
    Args:
        dt (datetime): The datetime to format
        
    Returns:
        str: ISO formatted datetime string
    """
    if not dt:
        return None
    return dt.isoformat()

def parse_datetime(dt_string):
    """
    Parse a datetime string from API requests
    
    Args:
        dt_string (str): ISO formatted datetime string
        
    Returns:
        datetime: Parsed datetime object
    """
    if not dt_string:
        return None
    try:
        return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
    except ValueError:
        # Try different format if ISO format fails
        return datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")

def get_ndvi_health_status(ndvi_value):
    """
    Convert NDVI value to health status label
    
    Args:
        ndvi_value (float): NDVI value between -1 and 1
        
    Returns:
        str: Health status (Low, Medium, High)
    """
    if ndvi_value is None:
        return "Unknown"
    
    if ndvi_value < 0.3:
        return "Low"
    elif ndvi_value < 0.6:
        return "Medium"
    else:
        return "High" 