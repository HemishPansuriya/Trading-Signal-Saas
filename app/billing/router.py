from fastapi import APIRouter, Depends,Header,Request,HTTPException
import stripe
from app.config import STRIPE_SECRET_KEY,STRIPE_WEBHOOK_SECRET
from app.auth.deps import get_current_user
from app.models import User
from app.database import SessionLocal
from app.redis_client import redis_client

router = APIRouter(prefix="/billing", tags=["Billing"])

# 🔑 THIS LINE FIXES YOUR ERROR
stripe.api_key = STRIPE_SECRET_KEY


@router.post("/create-checkout")
def create_checkout_session(
    current_user: User = Depends(get_current_user),
):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": "Premium Trading Signals",
                    },
                    "unit_amount": 49900,  # ₹499.00
                    "recurring": {
                        "interval": "month",
                    },
                },
                "quantity": 1,
            }
        ],
        success_url="http://localhost:5173/success",
        cancel_url="http://localhost:5173/cancel",
        customer_email=current_user.email,
    )

    return {
        "checkout_url": session.url
    }

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None)
):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload,
            stripe_signature,
            STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # ✅ Handle payment success
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session["customer_email"]

        # 🔁 Redis idempotency
        event_id = event["id"]
        if redis_client.get(event_id):
            return {"status": "duplicate ignored"}

        redis_client.setex(event_id, 3600, "processed")

        # 🧠 Mark user as paid
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_paid = True
            db.commit()
        db.close()

    return {"status": "success"}

