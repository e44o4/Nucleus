import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Read from environment variable — fallback to local dev URL if not set
# For production: set DATABASE_URL in your .env file or system environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nucleus_user:nucleus123@localhost/nucleus"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # automatically reconnect if DB connection drops
    pool_size=5,             # number of persistent connections in the pool
    max_overflow=10          # extra connections allowed beyond pool_size
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)