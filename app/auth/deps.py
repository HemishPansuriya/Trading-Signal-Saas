from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth.security import decode_token


# Dependency to get a database session
def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Provide the session to the request
        yield db
    finally:
        # Close the session after request is completed
        db.close()


# Dependency to get the currently authenticated user
def get_current_user(
    # Decode JWT token and extract payload (e.g., user ID)
    payload: dict = Depends(decode_token),
    
    # Get database session using dependency injection
    db: Session = Depends(get_db),
):
    # Extract user ID from token payload ("sub" usually stores user id)
    user_id = payload.get("sub")

    # If user ID is missing in token payload, token is invalid
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # Fetch user from database using extracted user ID
    user = db.query(User).filter(User.id == int(user_id)).first()

    # If no user exists with this ID, deny access
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Return the authenticated user object
    return user
