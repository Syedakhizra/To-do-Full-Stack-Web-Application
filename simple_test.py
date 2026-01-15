"""
Simple test to verify the API can be imported and basic functionality works
"""
from sqlmodel import SQLModel, select
from app.database import engine
from app.models.user import User
from app.models.task import Task
import uuid
from datetime import datetime

def test_database_connection():
    """Test basic database connection and operations"""
    print("Testing database connection...")

    # Create a user
    user = User(email="test@example.com", username="testuser")

    from sqlmodel import Session

    with Session(engine) as session:
        # Add user to database
        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"Created user with ID: {user.id}, email: {user.email}")

        # Create a task for this user
        task = Task(
            id=str(uuid.uuid4()),
            title="Test Task",
            description="This is a test task",
            completed=False,
            user_id=user.id
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        print(f"Created task with ID: {task.id}, title: {task.title}")

        # Query the task back
        statement = select(Task).where(Task.user_id == user.id)
        tasks = session.exec(statement).all()

        print(f"Retrieved {len(tasks)} tasks for user {user.id}")
        for t in tasks:
            print(f"- Task: {t.title} (completed: {t.completed})")

        # Clean up - delete the test data
        session.delete(task)
        session.delete(user)
        session.commit()

        print("SUCCESS: Database operations test completed successfully!")

if __name__ == "__main__":
    test_database_connection()