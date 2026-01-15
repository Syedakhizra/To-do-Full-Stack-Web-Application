<!-- SYNC IMPACT REPORT:
Version change: N/A (initial version) → 1.0.0
Modified principles: N/A
Added sections: Core Principles (6 principles), Key Standards, Constraints, Success Criteria
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-driven development
All implementation must strictly follow approved specs. No code shall be written without a corresponding approved specification document that outlines requirements, interfaces, and acceptance criteria.

### Agentic workflow compliance
Adhere to spec → plan → tasks → implementation workflow strictly. No manual coding is allowed outside this defined process. All development must follow the prescribed sequence to ensure traceability and quality.

### Security-first design
Authentication, authorization, and user isolation enforced by default. All user data must be properly isolated, with authentication and authorization checks applied to every user-facing operation.

### Deterministic behavior
APIs and UI must behave consistently across users and sessions. System behavior must be predictable and reproducible, with consistent responses to identical inputs.

### Full-stack coherence
Frontend, backend, and database must integrate without mismatches. All layers of the application must work together seamlessly with well-defined interfaces between components.

### Technology stack adherence
No deviation from the prescribed technology stack: Frontend: Next.js 16+ (App Router), Backend: Python FastAPI, ORM: SQLModel, Database: Neon Serverless PostgreSQL, Auth: Better Auth (JWT-based).

## Key Standards

No implementation without an approved spec and plan. All API behavior must be explicitly defined in specs. Authentication must use Better Auth with JWT tokens. All backend routes must validate JWT and enforce task ownership. All database queries must be user-scoped. REST APIs must follow HTTP semantics and status codes. Errors must be explicit, predictable, and documented. Frontend must consume APIs exactly as specified. No hard-coded secrets; environment variables only.

## Constraints

No manual coding; all code generated via Claude Code. All endpoints require valid JWT after authentication. Stateless backend authentication (JWT only). Multi-user support is mandatory. Data persistence required across sessions.

## Success Criteria

All three specs (Backend, Auth, Frontend) are fully implemented and integrated. Users can sign up, sign in, and manage only their own tasks. Unauthorized requests return 401 consistently. Task ownership is enforced on every CRUD operation. Application works end-to-end as a full-stack system. Specs, plans, and iterations are reviewable and traceable. Project passes hackathon evaluation based on process and correctness.

## Governance

This constitution supersedes all other development practices. All implementations must comply with these principles and standards. Amendments require explicit documentation, approval process, and migration plan when applicable. All pull requests and reviews must verify constitutional compliance. All development activities must follow the spec-driven workflow as outlined.

**Version**: 1.0.0 | **Ratified**: 2026-01-15 | **Last Amended**: 2026-01-15