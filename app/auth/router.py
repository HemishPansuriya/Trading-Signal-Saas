from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth.deps import get_current_user
from app.auth.schemas import SignupRequest, LoginRequest


# Create an API router for authentication-related endpoints
# All routes will start with /auth and be grouped under "Auth"
router = APIRouter(prefix="/auth", tags=["Auth"])


# Dependency to provide a database session
def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session to the API endpoint
        yield db
    finally:
        # Close the session after request completes
        db.close()


# Signup endpoint to register a new user
@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    # Check if a user with the given email already exists
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "User already exists")

    # Create a new user instance with hashed password
    user = User(
        email=data.email,
        password_hash=hash_password(data.password)
    )

    # Save user to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate and return a JWT access token for the new user
    return {"token": create_access_token(user.id)}


# Login endpoint to authenticate an existing user
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Fetch user from database by email
    user = db.query(User).filter(User.email == data.email).first()

    # Validate user existence and password
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    # Generate and return a JWT access token
    return {"token": create_access_token(user.id)}


# Protected endpoint to get current logged-in user's details
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    # Return basic user information
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_paid": current_user.is_paid
    }
