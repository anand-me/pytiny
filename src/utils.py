import re
from typing import Optional
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """
    Validate if the given string is a proper URL.
    
    Args:
        url: String to validate
        
    Returns:
        bool: True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def sanitize_url(url: str) -> Optional[str]:
    """
    Sanitize and normalize URL.
    
    Args:
        url: URL to sanitize
        
    Returns:
        Optional[str]: Sanitized URL or None if invalid
    """
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if validate_url(url):
        return url
    return None

def is_valid_code(code: str) -> bool:
    """
    Validate if the given string is a valid short code.
    
    Args:
        code: String to validate
        
    Returns:
        bool: True if valid code, False otherwise
    """
    return bool(re.match(r'^[a-zA-Z0-9]{4,12}$', code))
