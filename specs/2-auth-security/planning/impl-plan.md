# Implementation Plan: Todo Full-Stack Web Application Spec-2 (Authentication & Security)

**Feature**: 2-auth-security
**Created**: 2026-01-15
**Status**: Draft
**Author**: Claude Code

## Technical Context

The Todo Full-Stack Web Application Spec-2 implements secure authentication and authorization using Better Auth and JWT tokens. This feature builds upon the existing Spec-1 backend APIs to add user authentication and access control. The system will integrate Better Auth on the frontend to handle user registration and login, while the FastAPI backend will verify JWT tokens and enforce user-based access control.

The authentication flow involves Better Auth issuing JWT tokens upon successful authentication, which are then attached to all API requests from frontend to backend. The backend will verify JWT signatures using a shared secret and extract user identity to enforce proper access controls.

**Architecture Stack**:
- Frontend Authentication: Better Auth
- Token Type: JWT (JSON Web Tokens)
- Backend Framework: FastAPI
- Backend Language: Python
- Database: Neon Serverless PostgreSQL (existing from Spec-1)

**Key Challenges**:
- Integrating Better Auth with existing backend APIs from Spec-1
- Implementing JWT verification middleware for FastAPI
- Enforcing user-based access control for task operations
- Maintaining statelessness in token verification

## Constitution Check

**Principle**: Spec-driven development
**Status**: ✅ Compliant
**Evidence**: Following approved specification from specs/2-auth-security/spec.md

**Principle**: Agentic workflow compliance
**Status**: ✅ Compliant
**Evidence**: Adhering to spec → plan → tasks → implementation workflow

**Principle**: Security-first design
**Status**: ✅ Compliant
**Evidence**: Implementing JWT-based authentication and user isolation via token verification

**Principle**: Deterministic behavior
**Status**: ✅ Compliant
**Evidence**: Consistent JWT validation and access control responses

**Principle**: Full-stack coherence
**Status**: ✅ Compliant
**Evidence**: Following prescribed technology stack (Better Auth + FastAPI + Neon PostgreSQL)

**Principle**: Technology stack adherence
**Status**: ✅ Compliant
**Evidence**: Using prescribed stack: Better Auth for frontend auth, JWT tokens, FastAPI for backend verification

**Standards Compliance**:
- ✅ No implementation without approved spec and plan
- ✅ Authentication uses Better Auth with JWT tokens
- ✅ All backend routes verify JWT and enforce task ownership
- ✅ All database queries remain user-scoped
- ✅ REST APIs follow HTTP semantics and status codes
- ✅ Errors are explicit, predictable, and documented

## Phase 0: Research & Discovery

### Research Completed: JWT Authentication Patterns with Better Auth
**Outcome**: Successfully investigated best practices for integrating Better Auth with JWT token verification in FastAPI.

**Findings**:
- Better Auth handles JWT issuance and frontend management
- FastAPI can use middleware or dependencies for JWT verification
- Shared secret must be configured identically on frontend and backend
- JWT should contain user identity claims for authorization

### Research Completed: FastAPI JWT Verification Middleware Implementation
**Outcome**: Researched implementation patterns for JWT verification middleware in FastAPI applications.

**Findings**:
- Use python-jose library for JWT decoding and verification
- Create FastAPI dependency for JWT validation
- Extract user identity from token payload
- Return HTTP 401 for invalid/missing tokens

### Research Completed: User-Based Access Control Strategies
**Outcome**: Established patterns for enforcing user-based access control using JWT identity claims.

**Findings**:
- Extract user_id from JWT payload to verify ownership
- Compare authenticated user_id with resource user_id
- Return appropriate HTTP status codes (401, 403) for unauthorized access
- Integrate with existing user_id parameters in API endpoints

## Phase 1: Design & Architecture

### 1.1 Auth Flow Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Frontend      │────│   Better Auth    │────│   FastAPI Backend   │
│   (Next.js)     │    │   (JWT Issuer)   │    │   (JWT Verifier)    │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
         │                        │                        │
         │ 1. Register/Login      │                        │
         │────────────────────────▶│                        │
         │                        │ 2. Issue JWT Token     │
         │                        │────────────────────────▶│
         │                        │                        │
         │ 3. Attach JWT to req   │                        │
         │─────────────────────────────────────────────────▶│
         │                                                │
         │                                                │ 4. Verify JWT Signature
         │                                                │─────────────────▶│
         │                                                │◀─────────────────│
         │                                                │ 5. Extract User ID
         │                                                │
         │                                                │ 6. Verify Ownership
         │                                                │
         │                                                │ 7. Return Response
         │◀─────────────────────────────────────────────────────────────────│
```

### 1.2 JWT Token Structure

**Payload Fields**:
- `user_id` (String/Integer): Unique identifier for the authenticated user (required)
- `email` (String): User's email address (optional but recommended)
- `exp` (Integer): Unix timestamp for token expiration (required)
- `iat` (Integer): Unix timestamp for token issuance (required)
- `sub` (String): Subject identifier (optional)

**Token Configuration**:
- Algorithm: HS256 (symmetric signing with shared secret)
- Expiration: 7 days from issuance (604800 seconds)
- Secret: Shared between frontend (Better Auth) and backend (FastAPI)

### 1.3 Backend JWT Verification Middleware

#### JWT Verification Dependency
- **Location**: `backend/app/auth/jwt.py`
- **Function**: `verify_jwt_token(token: str = Security(get_jwt_header)) -> dict`
- **Responsibility**: Decode and verify JWT token, extract user identity
- **Output**: Dictionary containing user claims or raises HTTP 401

#### User Identity Extraction
- Extract `user_id` from token payload for authorization decisions
- Compare with resource owner for access control
- Store in request context for downstream handlers

### 1.4 API Contract Modifications

#### Protected Endpoints (Updated from Spec-1)
- **POST /api/v1/tasks**: Require valid JWT, use authenticated user_id
- **GET /api/v1/users/{user_id}/tasks**: Verify JWT user_id matches path user_id
- **GET /api/v1/users/{user_id}/tasks/{task_id}**: Verify JWT user_id matches resource owner
- **PUT /api/v1/users/{user_id}/tasks/{task_id}**: Verify JWT user_id matches resource owner
- **DELETE /api/v1/users/{user_id}/tasks/{task_id}**: Verify JWT user_id matches resource owner

#### New Authentication Endpoints
- **POST /api/v1/auth/verify**: Verify JWT token validity (for frontend health checks)

### 1.5 Error Handling Strategy
- **Invalid JWT**: HTTP 401 Unauthorized with "Invalid token" message
- **Expired Token**: HTTP 401 Unauthorized with "Token expired" message
- **Insufficient Permissions**: HTTP 403 Forbidden with "Access denied" message
- **Token Not Provided**: HTTP 401 Unauthorized with "Authorization header required"

**Consistent Error Format**:
```json
{
  "detail": "Human-readable error message",
  "status_code": 401,
  "timestamp": "ISO 8601 timestamp"
}
```

### 1.6 Security Considerations
- JWT signature verification using shared secret
- Token expiration validation
- User identity verification for resource access
- Protection against token replay attacks
- Secure storage of shared secret in environment variables

## Phase 2: Implementation Preparation

### 2.1 Development Environment Setup
- Add JWT libraries to requirements (python-jose, bcrypt)
- Configure shared secret in environment variables
- Update existing API endpoints to require authentication
- Set up middleware for token verification

### 2.2 Testing Strategy
- Unit tests for JWT verification functions
- Integration tests for protected endpoints
- Authentication flow tests
- User isolation verification tests

### 2.3 Migration Considerations
- Existing Spec-1 APIs will require authentication
- User_id parameters will be derived from JWT instead of request body
- Database user records may need to be linked with Better Auth users

## Success Criteria Validation

✅ **Users can register and sign in via Better Auth**: Integration with Better Auth will handle registration/login
✅ **JWT tokens issued and validated**: Backend will verify JWT signatures using shared secret
✅ **Protected routes reject unauthenticated requests**: All endpoints will return 401 for invalid tokens
✅ **Users access only their own tasks**: JWT user_id will be compared with resource ownership
✅ **Integration with existing Spec-1 APIs**: Minimal changes to existing API contracts while adding authentication
✅ **Stateless token verification**: Signature validation without database lookups