"""
Returns trading signals.
- JWT protected
- Uses Redis cache (5 minutes)
- Free vs Paid logic based on user subscription
"""

from fastapi import APIRouter, Depends
from app.redis_client import redis_client
from app.auth.deps import get_current_user
from app.models import User
import random
import json

router = APIRouter(prefix="/signals", tags=["Signals"])


@router.get("")
def get_signals(current_user: User = Depends(get_current_user)):
    """
    This endpoint:
    1. Requires user to be logged in (JWT)
    2. Fetches signals from Redis cache
    3. Returns limited/full signals based on payment
    """

    cache_key = "signals"

    # 1️⃣ Try to get signals from Redis cache
    cached = redis_client.get(cache_key)

    if cached:
        # Redis stores strings → convert back to Python list
        signals = json.loads(cached)
    else:
        # 2️⃣ Mock expensive signal calculation
        signals = [
            {"symbol": "NIFTY", "signal": random.choice(["BUY", "SELL"])},
            {"symbol": "BANKNIFTY", "signal": random.choice(["BUY", "SELL"])},
        ]

        # Store in Redis for 5 minutes (300 seconds)
        redis_client.setex(
            cache_key,
            300,
            json.dumps(signals)
        )

    # 3️⃣ Paid vs Free logic (IMPORTANT)
    if current_user.is_paid:
        return signals          # Paid user → full access
    else:
        return signals[:1]      # Free user → limited access
