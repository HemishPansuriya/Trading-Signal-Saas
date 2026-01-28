from fastapi import APIRouter, Request, Header, HTTPException
import stripe
from app.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from app.database import SessionLocal
from app.models import User
# from app.redis_client import redis_client


# Create an API router for billing-related endpoints
# All routes under this router will start with /billing
router = APIRouter(prefix="/billing", tags=["Billing"])


# Set Stripe secret API key
# This key is used to authenticate requests to Stripe's API
stripe.api_key = STRIPE_SECRET_KEY
