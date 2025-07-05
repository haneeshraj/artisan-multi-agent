"""
Custom filters for the Flask application.
"""

from markupsafe import Markup


def nl2br(value):
    """
    Convert newlines to HTML line breaks.
    
    Args:
        value (str): The text to convert.
    
    Returns:
        Markup: The text with newlines converted to <br> tags.
    """
    if not value:
        return ""
    
    value = value.replace('\n', '<br>')
    return Markup(value)
