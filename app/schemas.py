from pydantic import BaseModel
from typing import List, Optional

# --- Schemas for nested relationships ---
class ChannelBase(BaseModel):
    # This maps directly to your TransformedChannel ORM model
    channel_id: int
    channel_username: str
    channel_title: str

    class Config:
        from_attributes = True # Enable ORM mode for this nested model

class ImageBase(BaseModel):
    # FIX: This maps to TransformedProductImages.
    # The 'message_id' was changed to 'product_id' in models.py to match DBT output.
    product_id: int # Changed from message_id to product_id
    image_path: str

    class Config:
        from_attributes = True # Enable ORM mode for this nested model

# --- Main Product Schemas ---
class ProductBase(BaseModel):
    # These are attributes directly on TransformedProduct
    product_id: int
    product_name: str
    price_in_birr: Optional[float] = None
    channel_id: int # Include channel_id as a direct attribute of product for convenience
    date: str # Assuming date comes as a string from DB or you format it

    # Nested relationships
    channel: ChannelBase # Use the nested Pydantic model for channel relationship
    images: List[ImageBase] # Use the nested Pydantic model for images relationship

    class Config:
        from_attributes = True # Enable ORM mode to work with SQLAlchemy models

class ProductCreate(BaseModel):
    # This can be used for creating new products (might not need nested relations for creation)
    channel_id: int
    channel_username: str
    channel_title: str
    product_id: int
    product_name: str
    price_in_birr: Optional[float] = None

class ProductResponse(BaseModel):
    # This is your main response model for a list of products
    products: List[ProductBase] # List of ProductBase instances in response

    class Config:
        from_attributes = True


# --- Other Schemas (as per your previous schemas.py, with orm_mode fix) ---
# Note: The 'Product' class you had that just inherited from ProductBase
# is now essentially replaced by ProductBase itself if it's the final output model.
# You might not need Product(BaseModel) unless it adds further fields.

# Example for other potential schemas (adjust as needed based on your models)
class Channel(BaseModel):
    channel_id: int
    channel_username: str # Changed from channel_name for consistency with models.py
    channel_title: str

    class Config:
        from_attributes = True

class ChannelResponse(BaseModel):
    channels: List[Channel]

    class Config:
        from_attributes = True


# Sample Pydantic model for detection results
class Detection(BaseModel):
    id: int # Assuming an ID for the detection record itself
    product_id: int
    confidence: float
    image_path: str

    class Config:
        from_attributes = True