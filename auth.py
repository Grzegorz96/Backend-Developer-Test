from jose import jwt
from fastapi import HTTPException
import datetime
from sqlalchemy.orm import Session
from models import User

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"


def create_token(email: str):
    """
    Generates a JSON Web Token (JWT) for the given email address.
    Args:
        email (str): The email address to include in the token's payload.
    Returns:
        str: The encoded JWT as a string.
    The token includes the following claims:
        - "sub": The subject of the token, set to the provided email address.
        - "exp": The expiration time of the token, set to one hour from the current time.
    The token is signed using the SECRET_KEY and the specified ALGORITHM.
    """

    return jwt.encode(
        {
            "sub": email,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=1),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_token(token: str, db: Session):
    """
    This function provides authentication-related functionalities.

    Functions:
        verify_token(token: str, db: Session) -> User:
            Verifies the provided JWT token and returns the associated user.

            Parameters:
                token (str): The JWT token to be verified.
                db (Session): The database session to query the user.

            Returns:
                User: The user associated with the token if valid.

            Raises:
                HTTPException: If the token is invalid or the user is not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.email == payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
