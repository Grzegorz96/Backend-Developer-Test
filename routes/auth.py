from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserLogin
from auth import create_token

# Create a new APIRouter instance
router = APIRouter()


"""
Handles user signup.

Args:
    user (UserCreate): The user information for creating a new user.
    db (Session, optional): The database session dependency.

Raises:
    HTTPException: If the email is already registered.

Returns:
    dict: A dictionary containing the authentication token for the new user.
"""


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    return {"token": create_token(user.email)}


"""
Handles user sign-in.

Args:
    user (UserLogin): The user login details.
    db (Session, optional): The database session. Defaults to Depends(get_db).

Raises:
    HTTPException: If the user credentials are invalid.

Returns:
    dict: A dictionary containing the authentication token.
"""


@router.post("/signin")
def signin(user: UserLogin, db: Session = Depends(get_db)):
    db_user = (
        db.query(User)
        .filter(User.email == user.email, User.password == user.password)
        .first()
    )
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token(user.email)}
