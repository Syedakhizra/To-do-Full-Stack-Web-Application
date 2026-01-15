from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
from .jwt import verify_token, extract_user_id_from_token
from ..errors import ErrorResponse


# Initialize security scheme for JWT Bearer tokens
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Get the current user from the JWT token in the Authorization header
    """
    token = credentials.credentials

    try:
        payload = verify_token(token)
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - no user_id in token"
            )

        # Return user info extracted from token
        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "token": token
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Extract and return just the user_id from the JWT token
    """
    token = credentials.credentials
    user_id = extract_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - no user_id in token"
        )

    return user_id


def verify_jwt_token_optional(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[Dict]:
    """
    Verify JWT token but return None if invalid (for optional auth endpoints)
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        return {
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "token": token
        }
    except:
        return None