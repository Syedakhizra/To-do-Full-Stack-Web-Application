# Data Model: Todo Backend Core & Data Layer

**Feature**: 1-backend-tasks
**Date**: 2026-01-15

## Entity Definitions

### Task Entity

**Description**: Represents a user's task with title, description, completion status, and ownership information.

**Fields**:
- `id`: UUID primary key, auto-generated unique identifier
  - Type: UUID (string format)
  - Constraints: Required, Unique, Auto-generated
  - Purpose: Global unique identifier for the task

- `title`: Task title
  - Type: String (varchar(255))
  - Constraints: Required, Max length 255 characters
  - Purpose: Brief description of the task

- `description`: Task details
  - Type: Text (optional)
  - Constraints: Optional
  - Purpose: Extended description of the task

- `completed`: Task completion status
  - Type: Boolean
  - Constraints: Required, Default: false
  - Purpose: Indicates whether the task is completed

- `user_id`: Owner identifier
  - Type: Integer (foreign key reference to User.id)
  - Constraints: Required
  - Purpose: Links task to the user who owns it

- `created_at`: Creation timestamp
  - Type: DateTime (timezone-aware)
  - Constraints: Required, Auto-generated
  - Purpose: Tracks when the task was created

- `updated_at`: Last modification timestamp
  - Type: DateTime (timezone-aware)
  - Constraints: Required, Auto-updates
  - Purpose: Tracks when the task was last modified

**Relationships**:
- Many-to-One: Many tasks belong to one user (via user_id foreign key)

**Validation Rules**:
- Title must not be empty or whitespace-only
- Title must be less than 256 characters
- user_id must reference an existing user
- Task cannot be deleted if user doesn't own it

### User Entity (Foundation for future auth integration)

**Description**: Represents a system user who owns tasks. This entity is created to establish the foundation for user ownership relationships.

**Fields**:
- `id`: User identifier
  - Type: Integer (auto-increment primary key)
  - Constraints: Required, Unique, Auto-generated
  - Purpose: Unique identifier for the user

- `email`: User's email address
  - Type: String (varchar(255))
  - Constraints: Required, Unique
  - Purpose: Primary contact information and potential authentication identifier

- `username`: User's chosen display name
  - Type: String (varchar(50))
  - Constraints: Optional, Unique
  - Purpose: User's chosen display name

- `created_at`: Account creation timestamp
  - Type: DateTime (timezone-aware)
  - Constraints: Required, Auto-generated
  - Purpose: Tracks when the user account was created

- `updated_at`: Last account modification timestamp
  - Type: DateTime (timezone-aware)
  - Constraints: Required, Auto-updates
  - Purpose: Tracks when the user account was last modified

**Relationships**:
- One-to-Many: One user owns many tasks

## Database Schema

### Tables

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

### Indexes
- Index on `tasks.user_id`: Optimizes user-specific queries
- Index on `tasks.completed`: Optimizes completion status queries

### Constraints
- Foreign key constraint: Ensures tasks reference valid users
- Not-null constraints: Enforces required fields
- Unique constraints: Prevents duplicate emails/usernames

## State Transitions

### Task States
- **Pending** (completed = false): Task exists but is not completed
- **Completed** (completed = true): Task has been marked as completed

### Valid Transitions
- Pending → Completed: When user marks task as done
- Completed → Pending: When user reopens a completed task

## Query Patterns

### User-Specific Queries
- Retrieve all tasks for a user: `SELECT * FROM tasks WHERE user_id = ?`
- Retrieve completed tasks for a user: `SELECT * FROM tasks WHERE user_id = ? AND completed = true`
- Count user's tasks: `SELECT COUNT(*) FROM tasks WHERE user_id = ?`

### Task Management Queries
- Create new task: `INSERT INTO tasks (...) VALUES (...)`
- Update task: `UPDATE tasks SET ... WHERE id = ? AND user_id = ?`
- Delete task: `DELETE FROM tasks WHERE id = ? AND user_id = ?`

## Business Logic

### Data Integrity Rules
1. Users can only modify tasks they own (same user_id)
2. Task titles must be non-empty
3. Task ownership cannot be transferred between users
4. Deleting a user should cascade-delete their tasks (to be implemented in future spec)

### Performance Considerations
1. Use parameterized queries to prevent SQL injection
2. Index foreign keys and frequently queried columns
3. Implement pagination for large result sets
4. Use transactions for complex operations involving multiple records