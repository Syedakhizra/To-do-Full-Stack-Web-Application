from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool, QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", 'sqlite:///./todo_app.db')

# Create engine with appropriate settings based on database type
if DATABASE_URL.startswith("sqlite"):
    # SQLite settings
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Required for SQLite
        poolclass=StaticPool,  # Required for SQLite
        echo=False  # Set to True for debugging SQL queries
    )
else:
    # PostgreSQL settings for Neon Serverless
    from sqlalchemy.pool import QueuePool
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
        echo=False           # Set to True for debugging SQL queries
    )

def get_session():
    with Session(engine) as session:
        yield session