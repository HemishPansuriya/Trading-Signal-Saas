# from fastapi import APIRouter, Depends,Header,Request,HTTPException
# import stripe
# from app.config import STRIPE_SECRET_KEY,STRIPE_WEBHOOK_SECRET
# from app.auth.deps import get_current_user
# from app.models import User
# from app.database import SessionLocal
# from app.redis_client import redis_client

# router = APIRouter(prefix="/billing", tags=["Billing"])

# # 🔑 THIS LINE FIXES YOUR ERROR
# stripe.api_key = STRIPE_SECRET_KEY


# @router.post("/create-checkout")
# def create_checkout_session(
#     current_user: User = Depends(get_current_user),
# ):
#     session = stripe.checkout.Session.create(
#         payment_method_types=["card"],
#         mode="subscription",
#         line_items=[
#             {
#                 "price_data": {
#                     "currency": "inr",
#                     "product_data": {
#                         "name": "Premium Trading Signals",
#                     },
#                     "unit_amount": 49900,  # ₹499.00
#                     "recurring": {
#                         "interval": "month",
#                     },
#                 },
#                 "quantity": 1,
#             }
#         ],
#         success_url="http://localhost:5173/success",
#         cancel_url="http://localhost:5173/cancel",
#         customer_email=current_user.email,
#     )

#     return {
#         "checkout_url": session.url
#     }

# @router.post("/webhook")
# async def stripe_webhook(
#     request: Request,
#     stripe_signature: str = Header(None)
# ):
#     payload = await request.body()

#     try:
#         event = stripe.Webhook.construct_event(
#             payload,
#             stripe_signature,
#             STRIPE_WEBHOOK_SECRET
#         )
#     except stripe.error.SignatureVerificationError:
#         raise HTTPException(status_code=400, detail="Invalid signature")

#     # ✅ Handle payment success
#     if event["type"] == "checkout.session.completed":
#         session = event["data"]["object"]
#         email = session["customer_email"]

#         # 🔁 Redis idempotency
#         event_id = event["id"]
#         if redis_client.get(event_id):
#             return {"status": "duplicate ignored"}

#         redis_client.setex(event_id, 3600, "processed")

#         # 🧠 Mark user as paid
#         db = SessionLocal()
#         user = db.query(User).filter(User.email == email).first()
#         if user:
#             user.is_paid = True
#             db.commit()
#         db.close()

#     return {"status": "success"}

from fastapi import APIRouter, Depends, Header, Request, HTTPException
import stripe
from app.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from app.auth.deps import get_current_user
from app.models import User
from app.database import SessionLocal


# Create router for billing-related APIs
router = APIRouter(prefix="/billing", tags=["Billing"])

# Set Stripe secret API key
stripe.api_key = STRIPE_SECRET_KEY


# Create a Stripe Checkout Session for subscription payment
@router.post("/create-checkout")
def create_checkout_session(current_user: User = Depends(get_current_user)):
    # Create a Stripe Checkout session
    session = stripe.checkout.Session.create(
        # Allow card payments
        payment_method_types=["card"],

        # Subscription-based payment
        mode="subscription",

        # Define product and pricing details
        line_items=[
            {
                "price_data": {
                    "currency": "inr",  # Currency (Indian Rupees)
                    "product_data": {
                        "name": "Premium Trading Signals",
                    },
                    "unit_amount": 49900,  # Amount in paise (₹499.00)
                    "recurring": {"interval": "month"},  # Monthly subscription
                },
                "quantity": 1,
            }
        ],

        # Redirect user after successful payment
        success_url="http://localhost:5173/dashboard?paid=true",

        # Redirect user if payment is canceled
        cancel_url="http://localhost:5173/dashboard",

        # Prefill customer email using logged-in user
        customer_email=current_user.email,
    )

    # Return Stripe Checkout URL to frontend
    return {"checkout_url": session.url}


# Stripe webhook endpoint to handle payment events
@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None)  # Stripe signature header
):
    # Read raw request body (required for signature verification)
    payload = await request.body()

    try:
        # Verify webhook signature and construct event
        event = stripe.Webhook.construct_event(
            payload,
            stripe_signature,
            STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        # Reject request if signature is invalid
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle successful checkout session completion
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Get customer email from Stripe session
        email = session["customer_email"]

        # Create database session
        db = SessionLocal()

        # Find user by email
        user = db.query(User).filter(User.email == email).first()

        # Mark user as paid if not already
        if user and not user.is_paid:
            user.is_paid = True
            db.commit()

        # Close database session
        db.close()

    # Acknowledge webhook receipt
    return {"status": "success"}

