from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False)

    items = relationship("PurchaseItem", back_populates="product")


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    customer_email = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("PurchaseItem", back_populates="purchase")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    line_total = Column(Float, nullable=False)

    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product", back_populates="items")


class DenominationInventory(Base):
    __tablename__ = "denominations"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False, unique=True)
    available_count = Column(Integer, nullable=False)