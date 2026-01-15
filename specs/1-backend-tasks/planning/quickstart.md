# Quickstart Guide: Todo Backend Core & Data Layer

**Feature**: 1-backend-tasks
**Date**: 2026-01-15

## Overview

This guide provides a quick introduction to setting up and running the Todo Backend Core & Data Layer. The backend provides RESTful API endpoints for task management with user-scoped data using FastAPI, SQLModel, and Neon Serverless PostgreSQL.

## Prerequisites

- Python 3.9 or higher
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL account and connection details
- Git for version control

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Using Poetry (recommended):
```bash
poetry install
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
DEBUG=true
SECRET_KEY=your-secret-key-here
```

### 5. Initialize the Database
Run database migrations to create the necessary tables:
```bash
# Using alembic if available
alembic upgrade head

# Or run the initialization script if provided
python scripts/init_db.py
```

### 6. Run the Application
```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the provided script
python -m app.main
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Create a Task
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Task",
    "description": "This is a sample task",
    "user_id": 1
  }'
```

### Get All Tasks for a User
```bash
curl -X GET http://localhost:8000/api/v1/users/1/tasks
```

### Get a Specific Task
```bash
curl -X GET http://localhost:8000/api/v1/users/1/tasks/{task_id}
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/api/v1/users/1/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task Title",
    "completed": true
  }'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/v1/users/1/tasks/{task_id}
```

## Database Schema

The application uses two main tables:

1. **users** - Stores user information
   - id (Primary Key)
   - email
   - username
   - created_at
   - updated_at

2. **tasks** - Stores task information
   - id (Primary Key)
   - title
   - description
   - completed
   - user_id (Foreign Key to users)
   - created_at
   - updated_at

## Development Tips

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_tasks.py
```

### Code Formatting
The project uses black for code formatting:
```bash
black .
```

### Linting
The project uses ruff for linting:
```bash
ruff check .
ruff check . --fix
```

### API Documentation
Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify your Neon PostgreSQL connection string is correct
   - Check that your database credentials are valid
   - Ensure your IP is whitelisted if using Neon's IP allowlist

2. **Environment Variables Not Loading**
   - Ensure the `.env` file is in the correct directory
   - Verify the file is named `.env` and not `env` or `.env.txt`

3. **Port Already in Use**
   - Change the port number in the uvicorn command
   - Kill any existing processes using the port: `lsof -ti:8000 | xargs kill -9`

## Next Steps

1. Implement authentication (Spec-2) to secure endpoints
2. Add frontend integration (Spec-3)
3. Deploy to production environment
4. Set up monitoring and logging