"""
Handles password hashing and JWT token creation/verification
"""

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import JWT_SECRET


# Password hashing configuration using bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# JWT signing algorithm
ALGORITHM = "HS256"

# HTTP Bearer authentication (expects Authorization: Bearer <token>)
security = HTTPBearer()


# Hash a plain-text password before storing it in the database
def hash_password(password: str) -> str:
    # bcrypt only uses the first 72 characters
    return pwd_context.hash(password[:72])


# Verify a plain-text password against a stored hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Slice to 72 characters for bcrypt compatibility
    return pwd_context.verify(plain_password[:72], hashed_password)


# Create a JWT access token for a user
def create_access_token(user_id: int) -> str:
    # Token payload:
    # "sub" → subject (user ID)
    # "exp" → token expiration time
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    # Encode and sign the JWT using secret key and algorithm
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


# Decode and validate JWT token from Authorization header
def decode_token(
    # Automatically extracts Bearer token from request header
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    try:
        # Extract raw token string
        token = credentials.credentials

        # Decode token and validate signature & expiration
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])

        # Return decoded token payload
        return payload

    except JWTError:
        # Raised when token is invalid or expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
