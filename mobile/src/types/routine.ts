import { Equipment, Exercise, Muscle } from './exercise';

export interface RoutineRequest {
  target_muscles: Muscle[];
  duration_minutes: number;
  equipment: Equipment[];
  experience_level: 'beginner' | 'intermediate' | 'advanced';
  goal: 'general_fitness' | 'strength' | 'hypertrophy';
  exercise_count: number;
}
export interface RoutineItem {
  exercise_id: string;
  sets: number;
  rep_min: number;
  rep_max: number;
  exercise: Exercise;
}
export interface RoutineResponse {
  routine: { name: string; estimated_duration_minutes: number; exercises: RoutineItem[] };
  validation: { valid: boolean; errors: string[]; warnings: string[] };
}
