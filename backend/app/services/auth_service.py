from typing import Optional
from ..models.user import User, UserCreate
from ..database import engine
from sqlmodel import Session, select
import bcrypt
from ..auth.jwt import create_access_token
from datetime import timedelta


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')

    try:
        return bcrypt.checkpw(plain_password, hashed_password)
    except ValueError:
        return False


def get_password_hash(password: str) -> str:
    """
    Generate a hash for the given password
    """
    if isinstance(password, str):
        password = password.encode('utf-8')

    # Ensure password is not longer than 72 bytes (bcrypt limit)
    if len(password) > 72:
        password = password[:72]

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode('utf-8')


def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password
    """
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
            return None

        return user


def create_user(user_data: UserCreate) -> User:
    """
    Create a new user with hashed password
    """
    with Session(engine) as session:
        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create user object
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user


def create_access_token_for_user(user: User) -> str:
    """
    Create an access token for the given user
    """
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