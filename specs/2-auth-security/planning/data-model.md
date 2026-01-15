# Data Model: Todo Auth Security

**Feature**: 2-auth-security
**Date**: 2026-01-15

## Entity Definitions

### JWT Token Structure

**Description**: JSON Web Token structure for authentication with required claims for authorization.

**Claims**:
- `user_id`: String/Integer identifier for the authenticated user
  - Purpose: Primary identifier for authorization decisions
  - Constraints: Required, immutable during token lifetime

- `email`: String email address of the user
  - Purpose: Reference information for user identification
  - Constraints: Optional, immutable during token lifetime

- `exp`: Integer Unix timestamp for token expiration
  - Purpose: Defines when the token becomes invalid
  - Constraints: Required, must be in the future

- `iat`: Integer Unix timestamp for token issuance
  - Purpose: Track when the token was created
  - Constraints: Required, set at token creation time

- `sub`: String subject identifier (typically same as user_id)
  - Purpose: Identifies the principal (user) of the token
  - Constraints: Optional, typically matches user_id

### Authenticated User Context

**Description**: Runtime context for an authenticated user during API request processing.

**Fields**:
- `user_id`: Integer identifier of the authenticated user
  - Purpose: Primary key for authorization decisions
  - Source: Extracted from JWT token payload

- `email`: String email address of the authenticated user
  - Purpose: Reference information for logging and identification
  - Source: Extracted from JWT token payload

- `token_valid`: Boolean indicating token validity
  - Purpose: Whether the JWT token passed verification
  - Source: Result of JWT signature and expiration validation

## Integration with Existing Models

### Task Model (from Spec-1)
- **Owner Verification**: Compare authenticated user_id with task.user_id
- **Access Control**: Allow operations only when user_id matches
- **Creation**: Use authenticated user_id as task.user_id (instead of request parameter)

### User Model (from Spec-1)
- **Identity Mapping**: Link Better Auth user records with existing user records
- **Verification**: Validate user exists in database when JWT contains user_id

## State Transitions

### Authentication States
- **Unauthenticated**: No valid JWT token provided
- **Authenticated**: Valid JWT token verified with user identity extracted
- **Expired**: JWT token was valid but has expired
- **Invalid**: JWT token signature verification failed

### Valid Transitions
- Unauthenticated → Authenticated: Valid JWT token provided
- Authenticated → Expired: Token expiration time reached
- Any state → Invalid: Malformed or tampered token received

## Validation Rules

### JWT Token Validation
1. Signature verification using shared secret
2. Expiration check (current time < exp claim)
3. Issuer validation (if issuer claim present)
4. Audience validation (if audience claim present)

### Authorization Validation
1. User identity extraction from token
2. Resource ownership verification
3. Permission validation for requested operation

## Query Patterns

### User-Specific Queries (Enhanced)
- Original: Retrieve all tasks for a user_id parameter
- Enhanced: Retrieve all tasks for authenticated user_id (from JWT)
- Verification: Confirm JWT user_id matches requested user_id

### Task Access Verification
- Before: Verify user_id parameter matches task owner
- After: Verify authenticated user_id (from JWT) matches task owner
- Security: Prevent user_id parameter manipulation

## Business Logic

### Authentication Flow
1. User registers/logs in via Better Auth
2. Better Auth issues JWT token with user claims
3. Frontend includes token in Authorization header
4. Backend verifies JWT signature and extracts user identity
5. Authorization decisions made based on authenticated user_id

### Authorization Flow
1. JWT token extracted from Authorization header
2. Token signature verified using shared secret
3. Claims validated (expiration, etc.)
4. user_id extracted from token payload
5. Resource ownership verified against user_id
6. Operation permitted or denied based on verification