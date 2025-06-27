# app/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List # FIX: Add this import

# Import your SQLAlchemy ORM models
from app.models import TransformedProduct, TransformedChannel, TransformedProductImages

# Assuming ProductBase is imported from app.schemas
from app.schemas import ProductBase, ChannelBase, ImageBase

async def get_product_by_name(db: AsyncSession, product_name: str) -> List[TransformedProduct]:
    """
    Retrieves transformed products by name, eagerly loading related channel and images data.
    """
    # Build the query: select TransformedProduct
    stmt = (
        select(TransformedProduct)
        .options(
            selectinload(TransformedProduct.channel), # Eager load the 'channel' relationship
            selectinload(TransformedProduct.images)   # Eager load the 'images' relationship
        )
        .filter(TransformedProduct.product_name.ilike(f"%{product_name}%")) # Case-insensitive search
        .order_by(TransformedProduct.date.desc()) # Example ordering
    )

    result = await db.execute(stmt) # Execute the query asynchronously
    products = result.scalars().unique().all() # Get all results as unique ORM objects

    return products

# Add other CRUD functions as needed, ensuring they are async