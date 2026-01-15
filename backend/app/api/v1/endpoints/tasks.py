from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse
from app.services.task_service import (
    create_task, get_tasks_by_user, get_task_by_id_and_user,
    update_task, delete_task
)
from app.models.task import TaskCreate, TaskUpdate
from typing import List
import logging
from app.auth.dependencies import get_user_id

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_request: TaskCreateRequest,
    current_user_id: int = Depends(get_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task associated with the authenticated user
    """
    try:
        task_create = TaskCreate(
            title=task_request.title,
            description=task_request.description,
            completed=False,
            user_id=current_user_id  # Use authenticated user_id instead of request parameter
        )

        task = create_task(session, task_create)

        # Convert Task model to TaskResponse manually
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like UserNotFoundException)
        raise
    except Exception as e:
        logging.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while creating task"
        )


@router.get("/users/me/tasks", response_model=List[TaskResponse])
def get_current_user_tasks(
    current_user_id: int = Depends(get_user_id),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user
    """
    try:
        tasks = get_tasks_by_user(session, current_user_id)
        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
    except Exception as e:
        logging.error(f"Error getting tasks for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving tasks"
        )


@router.get("/users/me/tasks/{task_id}", response_model=TaskResponse)
def get_current_user_task(
    task_id: str,
    current_user_id: int = Depends(get_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by its ID for the authenticated user
    """
    try:
        task = get_task_by_id_and_user(session, task_id, current_user_id)
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like TaskNotFoundException)
        raise
    except Exception as e:
        logging.error(f"Error getting task {task_id} for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while retrieving task"
        )


@router.put("/users/me/tasks/{task_id}", response_model=TaskResponse)
def update_current_user_task(
    task_id: str,
    task_update_request: TaskUpdateRequest,
    current_user_id: int = Depends(get_user_id),
    session: Session = Depends(get_session)
):
    """
    Update an existing task for the authenticated user
    """
    try:
        task_update = TaskUpdate(
            title=task_update_request.title,
            description=task_update_request.description,
            completed=task_update_request.completed
        )

        task = update_task(session, task_id, current_user_id, task_update)
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like TaskNotFoundException)
        raise
    except Exception as e:
        logging.error(f"Error updating task {task_id} for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while updating task"
        )


@router.delete("/users/me/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user_task(
    task_id: str,
    current_user_id: int = Depends(get_user_id),
    session: Session = Depends(get_session)
):
    """
    Remove a task from the system for the authenticated user
    """
    try:
        delete_task(session, task_id, current_user_id)
        return
    except HTTPException:
        # Re-raise HTTP exceptions (like TaskNotFoundException)
        raise
    except Exception as e:
        logging.error(f"Error deleting task {task_id} for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while deleting task"
        )