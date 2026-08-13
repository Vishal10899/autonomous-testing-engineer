export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

export function getAuthToken() {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('ate_access_token');
  }
  return null;
}

export function setAuthToken(token) {
  if (typeof window !== 'undefined') {
    if (token) {
      localStorage.setItem('ate_access_token', token);
    } else {
      localStorage.removeItem('ate_access_token');
    }
  }
}

export async function apiFetch(endpoint, options = {}) {
  const token = getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      let errorMessage = data.detail || data.message || 'An unexpected error occurred';

      if (response.status === 401) {
        errorMessage = 'Your session has expired. Please sign in again.';
        setAuthToken(null);
      } else if (response.status === 403) {
        errorMessage = "You don't have permission to perform this action.";
      } else if (response.status === 404) {
        errorMessage = 'The requested resource was not found.';
      } else if (response.status === 409) {
        errorMessage = data.detail || 'This resource already exists.';
      } else if (response.status === 500) {
        errorMessage = 'Internal server error. Please try again.';
      }

      const error = new Error(errorMessage);
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  } catch (err) {
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      const networkError = new Error('Unable to connect to Autonomous Testing Engineer server. Please verify backend is running.');
      networkError.status = 0;
      throw networkError;
    }
    throw err;
  }
}
