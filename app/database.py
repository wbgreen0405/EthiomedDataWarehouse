# app/database.py

import os
import sys
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # Use async engine and session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Configure a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    logger.error("FATAL: One or more database environment variables (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME) are not set.")
    raise ValueError("Missing critical database environment variables. Application cannot start.")

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Use create_async_engine for async drivers
# Keep it global, but the connection test will be an async function
engine = create_async_engine(DATABASE_URL) # Now using create_async_engine directly

# Create an async session maker
# Note: sessionmaker creates sessions. AsyncSession is the session type.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession, # Specify AsyncSession for asynchronous operations
    expire_on_commit=False # Important for async operations
)

Base = declarative_base()

# --- Connection Test moved to an async function ---
async def check_db_connection():
    """
    Tests the database connection asynchronously during application startup.
    This function should be called from an @app.on_event("startup") handler in main.py.
    """
    try:
        logger.info(f"Attempting to connect to database using asyncpg at {DB_HOST}:{DB_PORT}/{DB_NAME}...")
        async with engine.connect() as connection: # Use async with for connection
            # CORRECT WAY to run a synchronous operation (like reflect) on an async connection
            # This is the line that needs to be updated:
            await connection.run_sync(Base.metadata.reflect) # FIX: Use .run_sync() for reflection
        logger.info("Database engine created and connection verified successfully with asyncpg.")
        return True
    except Exception as e:
        logger.critical(f"FATAL: Error connecting to the database with asyncpg: {e}")
        # Re-raise the exception to prevent the application from starting if DB connection fails
        raise RuntimeError(f"Failed to initialize database engine (asyncpg): {e}") from e

# --- Dependency to get asynchronous database session ---
async def get_db() -> AsyncSession: # Use async def and AsyncSession type hint
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close() # Use await for async close