# Quickstart Guide: Todo Auth Security Implementation

**Feature**: 2-auth-security
**Date**: 2026-01-15

## Overview

This guide provides a quick introduction to implementing authentication and security for the Todo Full-Stack Web Application. The system uses Better Auth for frontend authentication and JWT tokens for securing backend API endpoints.

## Prerequisites

- Complete Spec-1 (Backend Core & Data Layer) implementation
- Better Auth configured on the frontend
- Shared secret configured for JWT signing
- Python 3.9+ with FastAPI and related dependencies
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
# Additionally install JWT libraries:
pip install python-jose[cryptography] bcrypt
```

### 4. Configure Environment Variables
Update your `.env` file with JWT configuration:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
DEBUG=True
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days in minutes
JWT_SECRET=your-shared-jwt-secret-here
```

### 5. Update Backend with Authentication
The authentication system will be integrated into the existing backend structure.

## Integration with Existing Backend

### 1. Add JWT Utilities
Create `backend/app/auth/jwt.py` with JWT utility functions:
- Token creation and verification functions
- Secret key management
- User identity extraction

### 2. Create Authentication Dependencies
Create `backend/app/auth/dependencies.py` with FastAPI dependencies:
- JWT token verification dependency
- Current user extraction dependency
- Authentication middleware

### 3. Update API Endpoints
Modify existing endpoints to require authentication:
- Add authentication dependencies to routes
- Replace user_id parameters with authenticated user context
- Add authorization checks for resource access

### 4. Create New Authentication Endpoints
Add new endpoints for token verification and user management.

## API Usage with Authentication

### Authenticating Requests
After successful login through Better Auth:
```bash
curl -X GET http://localhost:8000/api/v1/users/me/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Creating a Task (Authenticated)
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "title": "Sample Task",
    "description": "This is a sample task"
  }'
```

### Updating a Task (Authenticated)
```bash
curl -X PUT http://localhost:8000/api/v1/users/me/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "title": "Updated Task Title",
    "completed": true
  }'
```

## Testing Authentication

### Unit Tests
Run JWT verification tests:
```bash
pytest tests/test_auth.py
```

### Integration Tests
Test authenticated endpoints:
```bash
pytest tests/test_authenticated_endpoints.py
```

### Manual Testing
1. Register/login through Better Auth frontend
2. Obtain JWT token
3. Use token to make authenticated API requests
4. Verify unauthorized requests return 401

## Development Tips

### Running with Authentication
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Token Verification
Use the auth verification endpoint to test token validity:
```bash
curl -X POST http://localhost:8000/api/v1/auth/verify \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Debugging Authentication
- Check that JWT_SECRET matches between frontend and backend
- Verify token expiration times
- Confirm user_id in token matches expected values
- Validate that Authorization header format is correct

## Security Best Practices

### JWT Security
- Use strong, randomly generated secrets
- Set appropriate expiration times
- Always validate tokens before granting access
- Never store sensitive data in JWT payloads

### User Isolation
- Always verify user_id matches resource owner
- Use parameterized queries to prevent injection
- Implement proper error handling to avoid information leakage

## Troubleshooting

### Common Issues

1. **401 Unauthorized Errors**
   - Verify JWT token is properly formatted
   - Check that SECRET_KEY and JWT_SECRET match configuration
   - Ensure token hasn't expired

2. **User Access Violations**
   - Confirm JWT contains correct user_id claim
   - Verify authorization logic compares correct identifiers
   - Check that resource owner matches authenticated user

3. **Token Validation Failures**
   - Verify shared secret configuration
   - Check JWT algorithm matches expected (HS256)
   - Ensure token format is "Bearer TOKEN_HERE"

## Next Steps

1. Complete frontend integration with Better Auth
2. Test end-to-end authentication flow
3. Implement refresh token mechanism (future enhancement)
4. Add role-based permissions (future enhancement)
5. Deploy to production environment