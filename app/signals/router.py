from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user
from app.models import User
import random


# Create router for trading signal related APIs
router = APIRouter(prefix="/signals", tags=["Signals"])


# Endpoint to fetch trading signals
@router.get("")
def get_signals(current_user: User = Depends(get_current_user)):
    # Generate trading signals randomly (demo/mock data)
    signals = [
        {"symbol": "NIFTY", "signal": random.choice(["BUY", "SELL"])},
        {"symbol": "BANKNIFTY", "signal": random.choice(["BUY", "SELL"])},
    ]

    # If the user is a paid subscriber, return all signals
    if current_user.is_paid:
        return signals
    else:
        # Free users get limited access (only first signal)
        return signals[:1]
