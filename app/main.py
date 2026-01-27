"""
Application entry point
"""

from fastapi import FastAPI
from app.database import Base, engine
from app.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

from app.signals.router import router as signals_router
from app.billing.router import router as billing_router
from app.billing.webhook import router as webhook_router
from fastapi.security import HTTPBearer
from app.config import UPSTASH_TOKEN,UPSTASH_URL
import requests

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trading Signals SaaS")

# ✅ CORS CONFIG (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite frontend
        "http://127.0.0.1:5173",
        "https://trading-signal-saas.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

headers = {
    "Authorization": f"Bearer {UPSTASH_TOKEN}",
    "Content-Type": "application/json"
}

def redis_get(key):
    url = f"{UPSTASH_URL}/get/{key}"
    res = requests.get(url, headers=headers)
    return res.json()

def redis_set(key, value):
    url = f"{UPSTASH_URL}/set/{key}/{value}"
    res = requests.post(url, headers=headers)
    return res.json()

@app.get("/")
def home():
    redis_set("visits", 1)
    data = redis_get("visits")
    return {"redis_data": data}

# ✅ Root health check endpoint
@app.get("/")
def root():
    return {
        "message": "Trading Signals SaaS Backend is running",
        "docs": "/docs"
    }

# 👇 This line is IMPORTANT (enables Swagger Authorize button)
security = HTTPBearer()


# Routers
app.include_router(auth_router)
app.include_router(signals_router)
app.include_router(billing_router)
app.include_router(webhook_router)