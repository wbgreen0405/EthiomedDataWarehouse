# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base # Ensure Base is imported from your database setup

class TransformedProduct(Base):
    __tablename__ = "transformed_product"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    price_in_birr = Column(Float)
    channel_id = Column(Integer, ForeignKey("transformed_channel.channel_id")) # Foreign key to channel
    date = Column(DateTime)
    # FIX: Remove message_id from here, as it's now represented by product_id
    # message_id = Column(Integer) # <--- REMOVE THIS LINE

    # Relationships
    channel = relationship("TransformedChannel", back_populates="products")
    images = relationship("TransformedProductImages", back_populates="product_message")

    def __repr__(self):
        return f"<TransformedProduct(product_name='{self.product_name}', price_in_birr={self.price_in_birr})>"

class TransformedChannel(Base):
    __tablename__ = "transformed_channel"

    channel_id = Column(Integer, primary_key=True, index=True)
    channel_username = Column(String, unique=True, index=True)
    channel_title = Column(String)

    # Relationship to products
    products = relationship("TransformedProduct", back_populates="channel")

    def __repr__(self):
        return f"<TransformedChannel(username='{self.channel_username}')>"

class TransformedProductImages(Base):
    __tablename__ = "transformed_product_images"

    # FIX: Change Foreign Key to product_id to match TransformedProduct and dbt output
    # The message_id in this table is typically the foreign key to the product it belongs to.
    # Since transformed_product.product_id is derived from message_id, we link here.
    product_id = Column(Integer, ForeignKey("transformed_product.product_id"), primary_key=True) # FIX: Use product_id, not message_id
    image_path = Column(String)

    # Relationship back to the product
    # FIX: Update back_populates to point to the correct relationship attribute if names change
    product_message = relationship("TransformedProduct", back_populates="images")

    def __repr__(self):
        return f"<TransformedProductImages(product_id={self.product_id}, path='{self.image_path}')>"