# Quickstart Guide: Frontend Development

## Project Setup

### Prerequisites
- Node.js 18+ installed
- Access to backend API (Spec-1) running at configured endpoint
- Access to authentication system (Spec-2)

### Installation
```bash
# Navigate to project directory
cd todo-frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Update environment variables
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
# NEXT_PUBLIC_JWT_SECRET=your-jwt-secret
```

### Environment Variables
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL
- `NEXT_PUBLIC_JWT_SECRET` - JWT verification secret (should match backend)

## Development Workflow

### Starting Development Server
```bash
npm run dev
```
Application will be available at http://localhost:3000

### Building for Production
```bash
npm run build
npm start
```

## Key Architecture Patterns

### Authentication Flow
1. User accesses protected route
2. Auth middleware checks for valid JWT in storage
3. If valid, allows access; if not, redirects to login
4. JWT automatically attached to all API requests

### API Client Usage
```typescript
// Example API call with automatic JWT injection
import { apiClient } from '@/lib/api-client';

const tasks = await apiClient.get('/users/me/tasks');
const newTask = await apiClient.post('/users/me/tasks', { title: 'New task' });
```

### Component Structure
- Shared UI components in `/components/ui`
- Auth-related components in `/components/auth`
- Task management components in `/components/tasks`
- Layout components in `/components/layout`

## Common Tasks

### Adding New Pages
1. Create new folder in `/app/` directory
2. Add `page.tsx` file with page content
3. If protected, wrap with `ProtectedRoute` component

### Making API Calls
1. Use the centralized `apiClient` for all requests
2. Errors are automatically handled by interceptors
3. JWT tokens are automatically included

### Managing State
1. Use React Context for global state (auth, notifications)
2. Use component state for local UI state
3. Use custom hooks for complex state logic