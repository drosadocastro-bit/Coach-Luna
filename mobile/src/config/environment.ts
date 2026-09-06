// Public app configuration only. Provider secrets must never be EXPO_PUBLIC_* values.
export const API_URL = (process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/$/, '');
