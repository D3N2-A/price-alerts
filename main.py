import asyncio
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

from db import Database
from scrapper import scrape_products


async def main():
    load_dotenv()

    # Initialize database
    db = Database(connection_string=os.getenv("POSTGRES_URL"))

    # Get list of products from database
    products = db.get_products()

    await scrape_products(products)


if __name__ == "__main__":
    asyncio.run(main())
