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
# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trading Signals SaaS")

# ✅ CORS CONFIG (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite frontend
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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