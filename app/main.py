# app/main.py (relevant section)

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session # Keep for now if old sync dependencies exist, but ideally use AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession for async db operations
from pydantic import BaseModel
from typing import List, Optional

# Corrected imports (assuming database.py, crud.py, schemas.py are in the 'app' directory)
from .database import get_db, check_db_connection # Import check_db_connection
from .crud import get_product_by_name
from .schemas import ProductBase, ProductResponse

app = FastAPI(title="Integrated V-BPE Inference API")

# --- FastAPI Startup Event ---
@app.on_event("startup")
async def startup_event():
    """
    Runs on application startup.
    Performs a database connection check.
    """
    await check_db_connection()
    # You might also create database tables here if they don't exist
    # from .database import Base, engine
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)


# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates and static files
templates = Jinja2Templates(directory="app/templates")

# Root endpoint to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint for "Get Raw Data"
@app.get("/raw-data")
def get_raw_data():
    # Replace with actual data retrieval logic later
    return {"message": "Raw data placeholder"}

# Endpoint for "Clean Raw Data"
@app.get("/clean-raw-data")
def clean_raw_data():
    # Replace with actual cleaning logic later
    return {"message": "Cleaned raw data placeholder"}

# Endpoint for "Transform Data"
@app.get("/transform-data")
def transform_data():
    # Replace with actual transformation logic later
    return {"message": "Data transformation placeholder"}

# Endpoint for "Load Data"
@app.get("/load-data")
def load_data():
    # Replace with actual loading logic later
    return {"message": "Data loading placeholder"}

# Endpoint for "Explore Data"
@app.get("/explore-data")
def explore_data():
    # Replace with actual exploration logic later
    return {"message": "Data exploration placeholder"}

# Endpoint for "Search by Product"
@app.get("/search-product/", response_model=List[ProductBase]) # response_model expects List[ProductBase]
async def search_product(product_name: str, db: AsyncSession = Depends(get_db)):
    print(f"Search requested for: {product_name}")  # Debug log
    try:
        # Retrieve products by name, eagerly loading relationships
        products = await get_product_by_name(db=db, product_name=product_name)

        # FIX: Directly return the list of ORM objects.
        # FastAPI/Pydantic will automatically handle the conversion
        # to the response_model (List[ProductBase]) due to from_attributes=True
        if products:
            # The 'products' list returned from CRUD already contains ORM objects
            # that have 'date', 'channel' and 'images' relationships loaded (due to selectinload).
            # FastAPI's response_model will handle the conversion, including nested Pydantic models.
            print(f"Products found (ORM objects): {products}") # Log ORM objects (for debugging)
            return products # Return the list of ORM objects directly
        else:
            raise HTTPException(status_code=404, detail="Product not found")

    except Exception as e:
        print(f"Error: {e}")  # Log the exception
        # For production, consider a less verbose error message:
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))


# This block is for directly running the file for local testing with Uvicorn.
# It should be at the very bottom of the file.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)