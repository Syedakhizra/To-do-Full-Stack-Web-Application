# API Contracts: Frontend-Backend Integration

## Authentication Endpoints

### POST /api/v1/auth/login
**Description**: Authenticate user and return JWT token
**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
**Response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```
**Response (401)**:
```json
{
  "detail": "Invalid credentials"
}
```

### POST /api/v1/auth/register
**Description**: Register new user account
**Request**:
```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "password": "securePassword123"
}
```
**Response (201)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 2,
    "email": "newuser@example.com",
    "username": "newuser"
  }
}
```
**Response (400)**:
```json
{
  "detail": "Email already registered"
}
```

## Task Management Endpoints

### GET /api/v1/users/me/tasks
**Description**: Get authenticated user's tasks
**Headers**:
```
Authorization: Bearer {jwt_token}
```
**Response (200)**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Sample task",
      "description": "Task description",
      "completed": false,
      "user_id": 1,
      "created_at": "2026-01-15T10:00:00Z",
      "updated_at": "2026-01-15T10:00:00Z"
    }
  ]
}
```
**Response (401)**: Unauthorized

### POST /api/v1/users/me/tasks
**Description**: Create new task for authenticated user
**Headers**:
```
Authorization: Bearer {jwt_token}
```
**Request**:
```json
{
  "title": "New task",
  "description": "Task description",
  "completed": false
}
```
**Response (201)**:
```json
{
  "id": 2,
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-15T11:00:00Z",
  "updated_at": "2026-01-15T11:00:00Z"
}
```
**Response (400)**:
```json
{
  "detail": "Title is required"
}
```
**Response (401)**: Unauthorized

### PUT /api/v1/users/me/tasks/{task_id}
**Description**: Update task for authenticated user
**Headers**:
```
Authorization: Bearer {jwt_token}
```
**Request**:
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```
**Response (200)**:
```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true,
  "user_id": 1,
  "created_at": "2026-01-15T10:00:00Z",
  "updated_at": "2026-01-15T12:00:00Z"
}
```
**Response (401)**: Unauthorized
**Response (403)**: Forbidden (task doesn't belong to user)
**Response (404)**: Task not found

### PATCH /api/v1/users/me/tasks/{task_id}/complete
**Description**: Toggle task completion status
**Headers**:
```
Authorization: Bearer {jwt_token}
```
**Request**:
```json
{
  "completed": true
}
```
**Response (200)**:
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Task description",
  "completed": true,
  "user_id": 1,
  "created_at": "2026-01-15T10:00:00Z",
  "updated_at": "2026-01-15T13:00:00Z"
}
```
**Response (401)**: Unauthorized
**Response (403)**: Forbidden (task doesn't belong to user)
**Response (404)**: Task not found

### DELETE /api/v1/users/me/tasks/{task_id}
**Description**: Delete task for authenticated user
**Headers**:
```
Authorization: Bearer {jwt_token}
```
**Response (204)**: No content
**Response (401)**: Unauthorized
**Response (403)**: Forbidden (task doesn't belong to user)
**Response (404)**: Task not found

## Error Response Format
All error responses follow this format:
```json
{
  "detail": "Human-readable error message"
}
```

## Authentication Requirements
- All task endpoints require valid JWT token in Authorization header
- Token must not be expired
- User ID in token must match the requested resource owner
- Invalid/expired tokens return 401 Unauthorized