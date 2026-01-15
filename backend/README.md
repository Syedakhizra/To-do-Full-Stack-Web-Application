# Todo Backend

This is the backend component of the Todo application built with FastAPI and SQLModel.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main FastAPI application
│   ├── database.py            # Database connection and session management
│   ├── errors.py              # Custom error handling
│   ├── models/                # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   └── task.py           # Task model
│   ├── schemas/               # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── task.py           # Task schemas
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   └── task_service.py   # Task service layer
│   └── api/
│       └── v1/
│           └── endpoints/
│               ├── __init__.py
│               └── tasks.py  # API routes for tasks
├── scripts/
│   ├── __init__.py
│   └── init_db.py           # Database initialization script
├── test_backend.py          # Backend functionality tests
└── __init__.py
```

## Features

- Create, read, update, and delete tasks
- User-scoped data isolation (users can only access their own tasks)
- RESTful API design with proper HTTP status codes
- Data persistence with PostgreSQL
- Async support for better performance

## Tech Stack

- **Backend Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **API Style**: RESTful
- **Language**: Python 3.9+

## Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Set up environment variables:
```bash
cp ../.env .env
# Edit .env with your database credentials
```

3. Initialize the database:
```bash
python scripts/init_db.py
```

## Running the Application

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Create a Task
```bash
POST /api/v1/tasks
Content-Type: application/json

{
  "title": "Sample Task",
  "description": "This is a sample task",
  "user_id": 1
}
```

### Get All Tasks for a User
```bash
GET /api/v1/users/{user_id}/tasks
```

### Get a Specific Task
```bash
GET /api/v1/users/{user_id}/tasks/{task_id}
```

### Update a Task
```bash
PUT /api/v1/users/{user_id}/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated Task Title",
  "completed": true
}
```

### Delete a Task
```bash
DELETE /api/v1/users/{user_id}/tasks/{task_id}
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Security Considerations

- User-scoped data access via user_id parameter
- Input validation on all endpoints
- SQL injection prevention through ORM usage
- All endpoints verify that users can only access resources they own