# README.md
```markdown
# PyTiny URL Shortener

A lightweight, dependency-minimal URL shortener written in Python. Create short, shareable URLs with optional expiration times.

## Features

- Create short URLs with custom length
- Optional URL expiration
- Track click statistics
- CLI and Python API
- No external service dependencies
- SQLite storage

## Installation

```bash
pip install pytiny
```

## Quick Start

```python
from pytiny import PyTiny

# Initialize shortener
shortener = PyTiny()

# Create a short URL that expires in 24 hours
code = shortener.create_short_url(
    "https://example.com/very/long/url",
    expire_hours=24
)

# Get the original URL
long_url = shortener.get_long_url(code)
```

## CLI Usage

```bash
# Create a short URL
pytiny shorten https://example.com/long/url

# Create with expiration
pytiny shorten https://example.com/long/url --expire 24

# Get URL stats
pytiny stats abc123
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
