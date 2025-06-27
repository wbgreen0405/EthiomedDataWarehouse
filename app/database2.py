# app/database.py

import os
import sys
import logging # Import logging module
# Import asynchronous SQLAlchemy components
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # Use async engine and session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
#import psycopg2  # No longer needed if using asyncpg

# Configure a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Prevent duplicate handlers if this script is run multiple times
if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Add the project root to the Python path
# This assumes the .env file is in the EthiomedDataWarehouse folder
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Load environment variables from .env file
# The .env file is expected in the project_root (EthiomedDataWarehouse/.env)
load_dotenv(os.path.join(project_root, '.env'))

# Database configuration - load from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Basic validation for essential DB variables
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    logger.error("FATAL: One or more database environment variables (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME) are not set. Please check your .env file.")
    # This will cause a graceful failure if env vars are missing
    raise ValueError("Missing critical database environment variables. Application cannot start.")


# Create a database URL (using asyncpg dialect)
DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}' # FIX: Changed to postgresql+asyncpg

# Initialize engine. Use create_async_engine for async drivers.
engine = create_async_engine(DATABASE_URL) # FIX: Changed to create_async_engine

# Create an async session maker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession, # FIX: Specify AsyncSession for asynchronous operations
    expire_on_commit=False # Important for async operations with SQLAlchemy
)

# Create a base class for declarative models
Base = declarative_base()


# --- Database connection test function (now asynchronous) ---
async def check_db_connection():
    """
    Tests the database connection asynchronously during application startup.
    This function should be called from an @app.on_event("startup") handler in main.py.
    """
    try:
        logger.info(f"Attempting to connect to database using asyncpg at {DB_HOST}:{DB_PORT}/{DB_NAME}...")
        async with engine.connect() as connection: # FIX: Use async with for connection
            # Perform a dummy query or reflection to ensure the connection is active
            # .run_sync() is needed to run synchronous SQLAlchemy operations (like reflect) on an async connection
            await connection.run_sync(Base.metadata.reflect) # FIX: Use .run_sync() for reflection
        logger.info("Database engine created and connection verified successfully with asyncpg.")
        return True
    except Exception as e:
        logger.critical(f"FATAL: Error connecting to the database with asyncpg: {e}")
        # Re-raise the exception to prevent the application from starting if DB connection fails
        raise RuntimeError(f"Failed to initialize database engine (asyncpg): {e}") from e


# --- Dependency to get asynchronous database session ---
async def get_db() -> AsyncSession: # FIX: Changed to async def and AsyncSession type hint
    """
    Dependency function to provide an asynchronous database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close() # FIX: Use await for async close