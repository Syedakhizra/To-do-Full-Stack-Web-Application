from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt
from fastapi import HTTPException, status
from .errors import InvalidTokenException, TokenExpiredException


# Get secret key and algorithm from environment
SECRET_KEY = os.getenv("JWT_SECRET", os.getenv("SECRET_KEY", "d9f3b1e7c6a842e2b1f9d8c4a7f35e01b9a0d6e3c8f24b57a9d0e1f2c3b4a5d6"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days default


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with the provided data
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Verify the JWT token and return the payload if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError as e:
        raise InvalidTokenException(f"Could not validate credentials: {str(e)}")


def verify_token_with_expiration_check(token: str):
    """
    Verify the JWT token and explicitly check expiration
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Explicitly check expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.utcfromtimestamp(exp):
            raise TokenExpiredException()

        return payload

    except JWTError as e:
        raise InvalidTokenException(f"Could not validate credentials: {str(e)}")


def extract_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user_id from the JWT token
    """
    try:
        payload = verify_token(token)
        user_id: int = payload.get("user_id")
        return user_id
    except:
        return None


def extract_user_identity_from_token(token: str) -> Optional[dict]:
    """
    Extract user identity information from the JWT token
    """
    try:
        payload = verify_token(token)
        user_identity = {
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "exp": payload.get("exp"),
            "iat": payload.get("iat"),
            "sub": payload.get("sub")
        }
        return user_identity
    except:
        return None


def is_token_valid(token: str) -> bool:
    """
    Check if the token is valid without raising exceptions
    """
    try:
        verify_token(token)
        return True
    except:
        return False


def is_token_expired(token: str) -> bool:
    """
    Check if the token is expired without raising exceptions
    """
    try:
        payload = verify_token(token)
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.utcfromtimestamp(exp):
            return True
        return False
    except:
        return True  # If we can't verify the token, treat it as expired