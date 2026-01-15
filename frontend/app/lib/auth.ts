// Utility functions for authentication

/**
 * Store the JWT token in localStorage
 */
export const setAuthToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', token);
  }
};

/**
 * Get the JWT token from localStorage
 */
export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
};

/**
 * Remove the JWT token from localStorage
 */
export const removeAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
  }
};

/**
 * Decode a JWT token to extract payload
 */
export const decodeToken = (token: string): any => {
  try {
    // Split the token to get the payload part (middle part)
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

/**
 * Check if the token is expired
 */
export const isTokenExpired = (token: string): boolean => {
  const decodedToken = decodeToken(token);
  if (!decodedToken || !decodedToken.exp) {
    return true; // If there's no expiration, consider it expired
  }

  // Expiration is in seconds, Date.now() is in milliseconds
  const currentTime = Math.floor(Date.now() / 1000);
  return decodedToken.exp < currentTime;
};

/**
 * Verify if the current token is still valid
 */
export const isTokenValid = (): boolean => {
  const token = getAuthToken();
  if (!token) {
    return false;
  }

  return !isTokenExpired(token);
};

/**
 * Get user ID from the token
 */
export const getUserIdFromToken = (): number | null => {
  const token = getAuthToken();
  if (!token) {
    return null;
  }

  const decodedToken = decodeToken(token);
  if (decodedToken && decodedToken.user_id) {
    return decodedToken.user_id;
  }

  return null;
};