from fastapi import APIRouter, Request, Header, HTTPException
import stripe
from app.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from app.database import SessionLocal
from app.models import User
from app.redis_client import redis_client

router = APIRouter(prefix="/billing", tags=["Billing"])

stripe.api_key = STRIPE_SECRET_KEY
