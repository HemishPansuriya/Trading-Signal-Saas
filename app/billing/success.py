from fastapi import APIRouter

router = APIRouter()

@router.get("/success")
def payment_success():
    """
    This page is shown after successful Stripe checkout.
    IMPORTANT: Payment confirmation happens via webhook, NOT here.
    """
    return {
        "message": "✅ Subscription successful!",
        "next": "You can now access premium signals"
    }
