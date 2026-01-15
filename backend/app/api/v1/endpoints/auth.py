from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict
from app.auth.dependencies import get_current_user
from app.auth.jwt import create_access_token
from app.services.auth_service import authenticate_user, create_user
from app.models.user import User, UserCreate, UserRead
from datetime import timedelta
from sqlmodel import Session
from app.database import get_session
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str


router = APIRouter()


@router.post("/login", response_model=Dict)
def login_user(request_data: LoginRequest, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token
    """
    user = authenticate_user(request_data.email, request_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token_for_user(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }


@router.post("/register", response_model=Dict)
def register_user(request_data: RegisterRequest, session: Session = Depends(get_session)):
    """
    Register a new user and return JWT token
    """
    # Check if user already exists
    existing_user = session.query(User).filter(User.email == request_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user_data = UserCreate(
        email=request_data.email,
        username=request_data.username,
        password=request_data.password
    )
    user = create_user(user_data)

    # Create access token
    access_token = create_access_token_for_user(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    }


@router.post("/verify", response_model=Dict)
def verify_auth_token(current_user: dict = Depends(get_current_user)):
    """
    Verify if the provided JWT token is valid and return user information
    """
    return {
        "authenticated": True,
        "user_id": current_user["user_id"],
        "email": current_user.get("email")
    }


def create_access_token_for_user(user: User) -> str:
    """
    Create an access token for the given user
    """
    from app.auth.jwt import create_access_token

    data = {
        "user_id": user.id,
        "email": user.email,
        "sub": str(user.id)
    }

    token = create_access_token(
        data=data,
        expires_delta=timedelta(days=7)  # 7 days expiry
    )

    return token