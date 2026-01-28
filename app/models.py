"""
Database tables live here.
"""

from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    """
    User table
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_paid = Column(Boolean, default=False)
