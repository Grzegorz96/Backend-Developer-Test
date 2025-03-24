from pydantic import BaseModel, EmailStr, field_validator
from fastapi import HTTPException

# Define the maximum text size as 1 MB
MAX_TEXT_SIZE = 1024 * 1024  # 1 MB


# Schema for user creation with email and password fields
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Schema for user login with email and password fields
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for post creation with a text field
class PostCreate(BaseModel):
    text: str

    # Validator to check the size of the text field
    @field_validator("text")
    def check_text_size(cls, v):
        # Raise an HTTPException if the text size exceeds the maximum limit
        if len(v.encode("utf-8")) > MAX_TEXT_SIZE:
            raise HTTPException(
                status_code=413, detail="Text is too large. Max size is 1 MB."
            )
        return v
