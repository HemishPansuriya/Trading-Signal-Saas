
"""
Creates database engine and session.
SQLAlchemy uses this to talk to DB.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed only for SQLite
)

# Create DB session
SessionLocal = sessionmaker(bind=engine, autoflush=False)

# Base class for models
Base = declarative_base()
