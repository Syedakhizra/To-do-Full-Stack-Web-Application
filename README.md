# Todo Full-Stack Web Application

This project implements a persistent task management system using FastAPI, SQLModel, and Neon Serverless PostgreSQL. The system provides RESTful API endpoints for task CRUD operations with user-scoped data handling.

## Backend Structure

The backend is located in the `backend/` directory and follows a clean, modular architecture:

```
backend/
├── app/
│   ├── main.py                 # Main FastAPI application
│   ├── database.py            # Database connection and session management
│   ├── errors.py              # Custom error handling
│   ├── models/                # SQLModel database models
│   │   ├── user.py           # User model
│   │   └── task.py           # Task model
│   ├── schemas/               # Pydantic request/response schemas
│   │   └── task.py           # Task schemas
│   ├── services/              # Business logic
│   │   └── task_service.py   # Task service layer
│   └── api/
│       └── v1/
│           └── endpoints/
│               └── tasks.py  # API routes for tasks
├── scripts/
│   └── init_db.py           # Database initialization script
└── test_backend.py          # Backend functionality tests
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

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Initialize the database:
```bash
cd backend
python scripts/init_db.py
```

## Running the Application

```bash
cd backend
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

## Database Schema

The application uses two main tables:

1. **users** - Stores user information
   - id (Primary Key)
   - email
   - username
   - created_at
   - updated_at

2. **tasks** - Stores task information
   - id (Primary Key, UUID)
   - title
   - description
   - completed
   - user_id (Foreign Key to users)
   - created_at
   - updated_at

## Security Considerations

- User-scoped data access via user_id parameter
- Input validation on all endpoints
- SQL injection prevention through ORM usage
- All endpoints verify that users can only access resources they own

## Testing

Run the backend tests:
```bash
cd backend
python test_backend.py
```

## Deployment

The project includes a Dockerfile for containerized deployment:

```bash
cd backend
docker build -t todo-backend .
docker run -p 8000:8000 todo-backend
```

## License

[Specify your license here]