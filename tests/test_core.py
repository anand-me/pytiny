import pytest
import os
import time
from pytiny import PyTiny
from pytiny.utils import validate_url, sanitize_url

@pytest.fixture
def shortener():
    """Create a test instance of PyTiny."""
    db_path = "test_pytiny.db"
    shortener = PyTiny(db_path)
    yield shortener
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

def test_create_short_url(shortener):
    """Test creating a short URL."""
    url = "https://example.com"
    code = shortener.create_short_url(url)
    assert len(code) == 6
    assert shortener.get_long_url(code) == url

def test_expired_url(shortener):
    """Test that expired URLs are not accessible."""
    url = "https://example.com"
    # Create URL that expires in 1 second
    code = shortener.create_short_url(url, expire_hours=1/3600)  # 1 second
    # Wait for expiration
    time.sleep(1.1)  # Wait slightly more than 1 second
    assert shortener.get_long_url(code) is None

def test_url_validation():
    """Test URL validation utility."""
    assert validate_url("https://example.com")
    assert not validate_url("not-a-url")
    assert sanitize_url("example.com") == "https://example.com"
