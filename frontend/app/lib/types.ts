// User-related types
export interface User {
  id: number;
  email: string;
  username?: string;
  created_at?: string;
  updated_at?: string;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface UserLoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface UserRegisterRequest {
  email: string;
  username: string;
  password: string;
}

export interface UserRegisterResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Task-related types
export interface Task {
  id: string;  // Task IDs are UUIDs (strings) in the backend
  title: string;
  description?: string;
  completed: boolean;
  user_id: number;  // User IDs are integers in the backend
  created_at: string;
  updated_at: string;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  completed?: boolean;
}

// Internal types for UI components
export interface TaskCreateRequest {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

// API-specific types that include required backend fields
export interface TaskCreateApiRequest {
  title: string;
  description?: string;
  user_id: number;  // User IDs are integers in the backend
  completed?: boolean;
}

export interface TaskListResponse {
  tasks: Task[];
}

// API response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiErrorResponse {
  detail: string;
}

// Authentication context types
export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, username: string, password: string) => Promise<void>;
  logout: () => void;
  verifyToken: () => Promise<boolean>;
}

// Form types
export interface LoginFormValues {
  email: string;
  password: string;
}

export interface SignupFormValues {
  email: string;
  username: string;
  password: string;
  confirmPassword: string;
}