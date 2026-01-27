from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth.security import hash_password, verify_password, create_access_token
from app.redis_client import redis_client
from app.auth.deps import get_current_user
from app.auth.schemas import SignupRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def rate_limit(key: str):
    try:
        count = redis_client.incr(key)
        redis_client.expire(key, 60)
        if count > 5:
            raise HTTPException(429, "Too many requests")
    except Exception:
        # If Redis is down, allow request (fail-open)
        pass



@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    rate_limit(f"signup:{data.email}")

    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "User already exists")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()

    return {
        "token": create_access_token(user.id)
    }


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    rate_limit(f"login:{data.email}")

    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password[:72], user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    return {
        "token": create_access_token(user.id)
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns logged-in user details
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_paid": current_user.is_paid
    }