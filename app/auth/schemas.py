
"""
Request/response schemas for authentication
These schemas validate and structure incoming request data
"""

from pydantic import BaseModel, EmailStr, Field


# Schema for user signup (registration) request
class SignupRequest(BaseModel):
    # Email field with built-in email validation
    email: EmailStr

    # Password field with length constraints
    # min_length=6 → minimum 6 characters required
    # max_length=72 → commonly used upper limit for password hashing
    password: str = Field(min_length=6, max_length=72)


# Schema for user login request
class LoginRequest(BaseModel):
    # Email field with built-in email validation
    email: EmailStr

    # Password field (no length validation here, just required)
    password: str
