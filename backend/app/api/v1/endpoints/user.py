from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_user_id
from app.models.user import User, UserRead
from app.database import engine
from sqlmodel import Session, select

router = APIRouter()


@router.get("/users/me", response_model=UserRead)
def get_current_user(current_user_id: int = Depends(get_user_id)):
    """
    Get information about the currently authenticated user
    """
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == current_user_id)).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Convert to UserRead format
        return UserRead(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at
        )