from sqlmodel import Session, select, update
from app.models.task import Task, TaskCreate, TaskUpdate
from app.models.user import User
from app.errors import TaskNotFoundException, UserNotFoundException, UnauthorizedAccessException
from typing import List, Optional
import uuid
from datetime import datetime

def create_task(session: Session, task_data: TaskCreate) -> Task:
    """Create a new task"""
    # Verify that the user exists
    user_exists = session.exec(select(User).where(User.id == task_data.user_id)).first()
    if not user_exists:
        raise UserNotFoundException(task_data.user_id)

    # Create task with a UUID
    task = Task(
        id=str(uuid.uuid4()),
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=task_data.user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks_by_user(session: Session, user_id: int) -> List[Task]:
    """Get all tasks for a specific user"""
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks

def get_task_by_id_and_user(session: Session, task_id: str, user_id: int) -> Task:
    """Get a specific task by its ID and user ID"""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise TaskNotFoundException(task_id)

    return task

def update_task(session: Session, task_id: str, user_id: int, task_update: TaskUpdate) -> Task:
    """Update a task for a specific user"""
    # First, verify the task exists and belongs to the user
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise TaskNotFoundException(task_id)

    # Update the task with the provided data
    update_data = task_update.dict(exclude_unset=True, exclude_none=True)
    for field, value in update_data.items():
        if value is not None:  # Double check that value is not None
            setattr(task, field, value)

    # Update the timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: str, user_id: int) -> bool:
    """Delete a task for a specific user"""
    # First, verify the task exists and belongs to the user
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise TaskNotFoundException(task_id)

    session.delete(task)
    session.commit()
    return True