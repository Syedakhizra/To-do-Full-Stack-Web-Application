# Research Document: Todo Auth Security Implementation

**Feature**: 2-auth-security
**Date**: 2026-01-15

## Research Summary

This document consolidates research findings for implementing the Todo Full-Stack Web Application authentication and security feature using Better Auth and JWT tokens with FastAPI backend.

## Decision: JWT Authentication Patterns with Better Auth

**Rationale**: Better Auth provides a secure and standardized way to handle user authentication while allowing us to customize JWT token usage for backend authorization.

**Implementation Strategy**:
- Better Auth handles user registration, login, and initial JWT issuance
- Frontend stores JWT token securely (HTTP-only cookies or secure local storage)
- All API requests include Authorization header with Bearer token
- Backend verifies JWT signature using shared secret
- User identity extracted from token payload for authorization decisions

## Decision: JWT Payload Fields Required by Backend

**Rationale**: The backend needs specific claims to make authorization decisions while maintaining security and efficiency.

**Fields Defined**:
- `user_id`: Primary identifier for the authenticated user (required for authorization)
- `email`: User's email address (optional, for reference)
- `exp`: Expiration timestamp (required for validation)
- `iat`: Issued at timestamp (optional, for audit trails)
- `sub`: Subject identifier (optional, typically same as user_id)

## Decision: Token Expiration Duration and Validation Rules

**Rationale**: Appropriate expiration balances security (limiting token lifetime) with usability (not requiring frequent re-authentication).

**Configuration**:
- Expiration: 7 days (604800 seconds) from issuance
- Algorithm: HS256 (HMAC with SHA-256) using shared secret
- Validation: Check signature, verify not expired, ensure issuer is trusted
- Refresh: Not implemented in this phase (users must re-authenticate)

## Decision: Strategy to Match JWT User Identity with user_id Parameter

**Rationale**: Critical for maintaining data security by ensuring users can only access resources they own.

**Implementation**:
- Extract `user_id` claim from JWT payload during token verification
- Compare with `user_id` parameter in API endpoints (path or query parameters)
- For task operations, verify the authenticated user_id matches the task's owner
- Return HTTP 403 Forbidden if user_id mismatch occurs

## Decision: FastAPI JWT Verification Middleware Implementation

**Rationale**: Centralized JWT verification ensures consistent security across all protected endpoints.

**Implementation Approach**:
- Create JWT verification dependency using FastAPI Security
- Use python-jose library for JWT decoding and verification
- Implement as dependency that can be injected into route handlers
- Return HTTP 401 Unauthorized for invalid tokens

## Alternatives Considered

**Alternative 1**: Session-based authentication
- Pros: Traditional approach, familiar to many developers
- Cons: Requires server-side state storage, doesn't meet statelessness requirement

**Alternative 2**: OAuth 2.0 with external providers
- Pros: Leverages established providers like Google, GitHub
- Cons: Doesn't meet Better Auth requirement, adds complexity

**Alternative 3**: Custom token format instead of JWT
- Pros: Could be simpler to implement
- Cons: Loses interoperability benefits of JWT standard

**Chosen Solution**: JWT with Better Auth + FastAPI verification
- Aligns with prescribed technology approach
- Maintains statelessness requirement
- Provides secure user identity extraction
- Integrates cleanly with existing backend APIs