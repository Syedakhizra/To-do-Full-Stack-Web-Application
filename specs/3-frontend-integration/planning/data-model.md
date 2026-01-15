# Data Model: Frontend State Management

## User State
**Entity**: UserState
**Fields**:
- `id`: number (user identifier from JWT payload)
- `email`: string (user's email address)
- `isLoggedIn`: boolean (authentication status)
- `isLoading`: boolean (auth verification in progress)
- `error`: string | null (auth-related errors)

**Validation**:
- Email must be valid email format
- User ID must be positive integer

## Task State
**Entity**: TaskState
**Fields**:
- `tasks`: Array<Task> (list of user's tasks)
- `loading`: boolean (task operations in progress)
- `error`: string | null (task operation errors)
- `selectedTaskId`: number | null (currently selected task)

**Relationships**:
- Each task belongs to one user (via JWT authentication)
- Tasks are filtered by authenticated user's ID

## Task Entity (Client-Side)
**Entity**: Task
**Fields**:
- `id`: number (unique task identifier)
- `title`: string (task title, required)
- `description`: string | null (task description, optional)
- `completed`: boolean (completion status)
- `created_at`: string (ISO date string)
- `updated_at`: string (ISO date string)

**Validation**:
- Title must be 1-255 characters
- Description must be 0-1000 characters if provided
- Completed must be boolean

## Application State
**Entity**: AppState
**Fields**:
- `globalLoading`: boolean (overall app loading state)
- `notification`: Notification | null (user notifications)
- `currentPage`: string (current route for analytics)

## Notification Entity
**Entity**: Notification
**Fields**:
- `id`: string (unique identifier)
- `message`: string (notification text)
- `type`: 'success' | 'error' | 'info' | 'warning' (notification category)
- `timestamp`: Date (when notification was created)
- `duration`: number | null (milliseconds to auto-dismiss, null for persistent)

## Authentication Session
**Entity**: AuthSession
**Fields**:
- `token`: string (JWT token string)
- `expiresAt`: Date (token expiration time)
- `refreshToken`: string | null (if refresh tokens are implemented)
- `lastVerified`: Date (last successful auth verification)

**State Transitions**:
- Unauthenticated → Authenticating (during login/signup)
- Authenticating → Authenticated (successful login)
- Authenticating → Unauthenticated (failed login)
- Authenticated → Unauthenticated (logout/expired token)