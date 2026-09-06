export type Language = 'en' | 'es';
export type Muscle = 'quads' | 'glutes' | 'hamstrings' | 'calves' | 'erectors' | 'chest' | 'shoulders' | 'upper_back' | 'lats' | 'biceps' | 'triceps' | 'forearms' | 'core';
export type Equipment = 'dumbbells' | 'bench' | 'step' | 'mat' | 'cable_machine' | 'barbell';
export interface Exercise {
  id: string;
  name: string;
  display_name_es: string;
  primary_muscles: Muscle[];
  secondary_muscles: Muscle[];
  equipment: Equipment[];
  movement_pattern: 'squat' | 'hinge' | 'lunge' | 'bridge' | 'horizontal_push' | 'vertical_push' | 'horizontal_pull' | 'pullover' | 'isolation' | 'carry' | 'rotation' | 'anti_extension';
  difficulty: 'beginner' | 'beginner_intermediate' | 'intermediate' | 'advanced';
  unilateral: boolean;
  default_sets: number;
  rep_min: number;
  rep_max: number;
  prescription_unit: 'reps' | 'steps';
  video: { type: 'mp4'; uri: string | null; angles: ('front' | 'side' | 'rear' | 'three_quarter')[] };
  instructions_en: string[];
  instructions_es: string[];
  common_mistakes_en: string[];
  common_mistakes_es: string[];
  alternatives: string[];
  enabled: boolean;
}
