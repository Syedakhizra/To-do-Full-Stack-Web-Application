"""
Basic tests to verify the API functionality
"""
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import SQLModel, create_engine
from app.database import engine
from app.models.user import User
from app.models.task import Task

# Create test client
client = TestClient(app)

def test_create_and_retrieve_task():
    """Test creating a task and retrieving it"""

    # First create a user (in a real app, this would be done through user registration)
    user_response = client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "username": "testuser"
    })

    # For now, let's test with a hardcoded user_id = 1
    user_id = 1

    # Test creating a task
    create_response = client.post("/api/v1/tasks", json={
        "title": "Test Task",
        "description": "This is a test task",
        "user_id": user_id
    })

    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task["title"] == "Test Task"
    assert created_task["description"] == "This is a test task"
    assert created_task["user_id"] == user_id

    task_id = created_task["id"]

    # Test retrieving the task
    get_response = client.get(f"/api/v1/users/{user_id}/tasks/{task_id}")
    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Test Task"

    # Test retrieving all tasks for the user
    get_all_response = client.get(f"/api/v1/users/{user_id}/tasks")
    assert get_all_response.status_code == 200
    tasks_list = get_all_response.json()
    assert len(tasks_list) >= 1
    assert any(task["id"] == task_id for task in tasks_list)

def test_update_task():
    """Test updating a task"""

    # For this test, we'll need to have a user and task first
    user_id = 1
    task_title = "Initial Task"

    # Create a task first
    create_response = client.post("/api/v1/tasks", json={
        "title": task_title,
        "description": "Initial description",
        "user_id": user_id
    })

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Update the task
    update_response = client.put(f"/api/v1/users/{user_id}/tasks/{task_id}", json={
        "title": "Updated Task",
        "description": "Updated description",
        "completed": True
    })

    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["completed"] is True

def test_delete_task():
    """Test deleting a task"""

    user_id = 1

    # Create a task first
    create_response = client.post("/api/v1/tasks", json={
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "user_id": user_id
    })

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Delete the task
    delete_response = client.delete(f"/api/v1/users/{user_id}/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Verify the task is gone
    get_response = client.get(f"/api/v1/users/{user_id}/tasks/{task_id}")
    assert get_response.status_code == 404

if __name__ == "__main__":
    # Run basic functionality tests
    print("Testing API functionality...")

    try:
        test_create_and_retrieve_task()
        print("✓ Task creation and retrieval works")

        test_update_task()
        print("✓ Task update works")

        test_delete_task()
        print("✓ Task deletion works")

        print("\nAll tests passed!")
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")