import uuid
from sqlalchemy import JSON, Boolean, Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel

Base = declarative_base()


class DictMixin:
    """Mixin class to add as_dict capability to all models."""

    def as_dict(self):
        return {
            col.name: str(getattr(self, col.name)) for col in self.__table__.columns
        }


class Product(Base, DictMixin):
    __tablename__ = "products"
    url = Column(String, primary_key=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    prices = relationship(
        "PriceHistory", back_populates="product", cascade="all, delete-orphan"
    )


class PriceHistory(Base, DictMixin):
    __tablename__ = "price_history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_url = Column(String, ForeignKey("products.url"))
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    main_image_url = Column(String)
    availability = Column(Boolean, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    product = relationship("Product", back_populates="prices")
    additional_data = Column(JSON, nullable=True, default={})


class AIScrapperResult(BaseModel):
    title: str
    price: str
    currency: str
    image_url: str
    availability: bool
    additional_data: dict
