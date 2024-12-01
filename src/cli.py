import argparse
import sys
from datetime import datetime
from .core import PyTiny
from .utils import sanitize_url

def main():
    parser = argparse.ArgumentParser(description="PyTiny URL Shortener CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Shorten command
    shorten_parser = subparsers.add_parser("shorten", help="Shorten a URL")
    shorten_parser.add_argument("url", help="URL to shorten")
    shorten_parser.add_argument(
        "--expire", 
        type=int, 
        help="Expiration time in hours"
    )

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get URL statistics")
    stats_parser.add_argument("code", help="Short code to check")

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)

    shortener = PyTiny()

    if args.command == "shorten":
        url = sanitize_url(args.url)
        if not url:
            print("Error: Invalid URL")
            sys.exit(1)
            
        code = shortener.create_short_url(url, expire_hours=args.expire)
        print(f"Short URL: http://your-domain/{code}")

    elif args.command == "stats":
        stats = shortener.get_stats(args.code)
        if not stats:
            print("Error: Code not found")
            sys.exit(1)
            
        print("\nURL Statistics:")
        print(f"Created: {stats['created_at']}")
        print(f"Expires: {stats['expires_at'] or 'Never'}")
        print(f"Clicks: {stats['clicks']}")
        print(f"Last clicked: {stats['last_clicked'] or 'Never'}")

if __name__ == "__main__":
    main()
