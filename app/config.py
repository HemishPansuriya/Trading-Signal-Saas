# app/config.py
"""
This file stores all configuration values.
In production these come from environment variables.
"""

import os
import requests

# Database (SQLite for local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")

# JWT secret key (used to sign login tokens)
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Stripe keys (will be added later)
import os
UPSTASH_URL = os.getenv("UPSTASH_REDIS_REST_URL","https://living-quetzal-42747.upstash.io")
UPSTASH_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN","Aab7AAIncDJhMTQ5NmFiMjhiMDY0NjY4ODZiZTQyZmZjNzkyMWViYXAyNDI3NDc")

JWT_SECRET = os.getenv("JWT_SECRET", "super-secret")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHED_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

