export interface MediaVideo {
  type: 'video';
  url: string;
  angle: string;
  available_angles: string[];
}

export interface MediaResponse {
  exercise_id: string;
  available: boolean;
  provider: string | null;
  canonical: MediaVideo | null;
  alternates: Record<string, unknown>[];
}
