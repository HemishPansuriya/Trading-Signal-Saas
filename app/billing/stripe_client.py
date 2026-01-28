import stripe
from app.config import STRIPE_SECRET_KEY

# Set the Stripe API secret key
# This key is used to authenticate all Stripe API requests
stripe.api_key = STRIPE_SECRET_KEY
