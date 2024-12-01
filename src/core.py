import sqlite3
import string
import random
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple
from pathlib import Path

class PyTiny:
    """
    A lightweight URL shortener implementation with optional link expiration.
    """
    
    def __init__(self, db_path: str = "pytiny.db"):
        self.db_path = db_path
        self._init_db()
        
        # Characters to use for short URLs (excluding similar looking ones)
        self.chars = string.ascii_letters + string.digits
        self.chars = self.chars.replace('1', '').replace('l', '').replace('I', '')
        self.chars = self.chars.replace('0', '').replace('O', '').replace('o', '')
        
    def _init_db(self) -> None:
        """Initialize SQLite database with required schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    short_code TEXT UNIQUE NOT NULL,
                    long_url TEXT NOT NULL,
                    created_at INTEGER NOT NULL,
                    expires_at INTEGER,
                    clicks INTEGER DEFAULT 0,
                    last_clicked INTEGER
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_short_code ON urls(short_code)")
    
    def _generate_code(self, length: int = 6) -> str:
        """Generate a unique short code."""
        while True:
            code = ''.join(random.choices(self.chars, k=length))
            # Check if code already exists
            with sqlite3.connect(self.db_path) as conn:
                exists = conn.execute(
                    "SELECT 1 FROM urls WHERE short_code = ?", (code,)
                ).fetchone()
                if not exists:
                    return code
    
    def create_short_url(self, 
                        long_url: str, 
                        expire_hours: Optional[int] = None) -> str:
        """
        Create a new short URL.
        
        Args:
            long_url: The URL to shorten
            expire_hours: Optional expiration time in hours
            
        Returns:
            str: The generated short code
        """
        code = self._generate_code()
        now = int(time.time())
        expires_at = None
        
        if expire_hours:
            expires_at = now + (expire_hours * 3600)
            
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO urls (short_code, long_url, created_at, expires_at)
                VALUES (?, ?, ?, ?)
            """, (code, long_url, now, expires_at))
            
        return code
    
    def get_long_url(self, short_code: str) -> Optional[str]:
        """
        Retrieve the original URL and update click statistics.
        Returns None if code doesn't exist or has expired.
        """
        now = int(time.time())
        
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("""
                SELECT long_url, expires_at 
                FROM urls 
                WHERE short_code = ?
            """, (short_code,)).fetchone()
            
            if not result:
                return None
                
            long_url, expires_at = result
            
            # Check expiration more strictly
            if expires_at is not None and expires_at <= now:
                # URL has expired
                return None
            
            # Update click statistics only if not expired
            conn.execute("""
                UPDATE urls 
                SET clicks = clicks + 1,
                    last_clicked = ?
                WHERE short_code = ?
            """, (now, short_code))
            
        return long_url
    
    def get_stats(self, short_code: str) -> Optional[dict]:
        """Get usage statistics for a short URL."""
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("""
                SELECT created_at, expires_at, clicks, last_clicked
                FROM urls
                WHERE short_code = ?
            """, (short_code,)).fetchone()
            
            if not result:
                return None
                
            created_at, expires_at, clicks, last_clicked = result
            
            return {
                "created_at": datetime.fromtimestamp(created_at),
                "expires_at": datetime.fromtimestamp(expires_at) if expires_at else None,
                "clicks": clicks,
                "last_clicked": datetime.fromtimestamp(last_clicked) if last_clicked else None
            }
    
    def cleanup_expired(self) -> int:
        """Remove expired URLs from database. Returns number of URLs removed."""
        now = int(time.time())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM urls
                WHERE expires_at IS NOT NULL
                AND expires_at <= ?
            """, (now,))
            
        return cursor.rowcount

    def delete_url(self, short_code: str) -> bool:
        """
        Delete a URL by its short code.
        
        Args:
            short_code: The short code to delete
            
        Returns:
            bool: True if URL was deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM urls
                WHERE short_code = ?
            """, (short_code,))
            
        return cursor.rowcount > 0

    def update_expiry(self, short_code: str, expire_hours: Optional[int]) -> bool:
        """
        Update the expiration time of a URL.
        
        Args:
            short_code: The short code to update
            expire_hours: New expiration time in hours, None for no expiration
            
        Returns:
            bool: True if URL was updated, False if not found
        """
        now = int(time.time())
        expires_at = None
        
        if expire_hours is not None:
            expires_at = now + (expire_hours * 3600)
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                UPDATE urls
                SET expires_at = ?
                WHERE short_code = ?
            """, (expires_at, short_code))
            
        return cursor.rowcount > 0

if __name__ == "__main__":
    # Example usage
    shortener = PyTiny()
    code = shortener.create_short_url("https://example.com", expire_hours=24)
    print(f"Created short URL code: {code}")
    
    # Get the original URL
    long_url = shortener.get_long_url(code)
    print(f"Original URL: {long_url}")
    
    # Get statistics
    stats = shortener.get_stats(code)
    print(f"URL Statistics: {stats}")
