from sqlmodel import SQLModel
from app.database import engine
from app.models.user import User
from app.models.task import Task

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()