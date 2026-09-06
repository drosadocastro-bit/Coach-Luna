import { API_URL } from '../config/environment';
import { Exercise } from '../types/exercise';
import { RoutineRequest, RoutineResponse } from '../types/routine';

export class ApiError extends Error {
  constructor(public kind: 'network' | 'request' | 'server', message: string) { super(message); }
}

async function request<T>(path: string, body?: RoutineRequest): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(`${API_URL}${path}`, {
      method: body ? 'POST' : 'GET', signal: controller.signal,
      headers: { 'Content-Type': 'application/json' },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });
    if (!response.ok) throw new ApiError(response.status < 500 ? 'request' : 'server', `API request failed (${response.status})`);
    return await response.json() as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError('network', 'Backend unavailable or request timed out');
  } finally { clearTimeout(timeout); }
}

export const coachLunaApi = {
  generate: async (body: RoutineRequest) => {
    const response = await request<RoutineResponse>('/routines/generate', body);
    if (!response.validation?.valid || !Array.isArray(response.routine?.exercises)) throw new ApiError('server', 'Backend returned an unvalidated routine');
    return response;
  },
  exercise: (id: string) => request<Exercise>(`/exercises/${encodeURIComponent(id)}`),
};
