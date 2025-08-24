import asyncio
import os
from dotenv import load_dotenv

from db import Database
from scrapper import scrape_products


async def main():
    load_dotenv()

    # Initialize database
    print("Started fetching products from database")
    db = Database(connection_string=os.getenv("POSTGRES_URL"))

    # Get list of products from database
    products = db.get_products()

    await scrape_products(products, db)


if __name__ == "__main__":
    asyncio.run(main())
