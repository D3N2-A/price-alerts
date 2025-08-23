import os
import sys
from pathlib import Path

# Add parent directory to path so we can import from parent modules
sys.path.append(str(Path(__file__).parent.parent))

from utils.url import is_valid_url
from dotenv import load_dotenv
from db import Database


def add_product():
    """Interactive script to add a product URL to the database."""
    load_dotenv()

    # Initialize database
    db = Database(connection_string=os.getenv("POSTGRES_URL"))

    while True:
        print("\nEnter a product URL to track (or press Enter to quit):")
        url = input().strip()

        if not url:
            print("Exiting...")
            break

        # Basic URL validation
        if not is_valid_url(url):
            print("Error: Please enter a valid URL")
            continue

        # Add the product
        db.add_product(url)


if __name__ == "__main__":
    add_product()
