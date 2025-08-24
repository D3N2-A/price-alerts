import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import dumps, loads

from models import Base, PriceHistory, Product


class Database:

    def __init__(self, connection_string: str):
        try:
            self.engine = create_engine(connection_string)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            print(f"\nFailed to initialize database\n: {e}")
            raise e

    def add_product(self, url):
        session = self.Session()

        try:
            product = Product(url=url)
            session.merge(product)
            session.commit()
            print(f"Product added: {product.url}")
        except Exception as e:
            print(f"\nFailed to add product\n: {e}")
        finally:
            session.close()

    def get_products(self):
        session = self.Session()

        try:
            products = (
                session.query(Product)
                .filter(Product.is_active.is_(True))
                .filter(Product.is_deleted.isnot(True))
                .all()
            )
            session.close()
            return [product.as_dict() for product in products]
        except Exception as e:
            print(f"\nFailed to get products\n: {e}")
        finally:
            session.close()

    def store_price_history(self, price_history: PriceHistory):
        session = self.Session()

        try:
            session.add(price_history)
            session.commit()
        except Exception as e:
            print(f"\nFailed to store price history\n: {e}")
            session.rollback()
        finally:
            session.close()
