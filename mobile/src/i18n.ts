import { Language } from './types/exercise';

const labels: Record<string, [string, string]> = {
  quads: ['Quads', 'Cuádriceps'], glutes: ['Glutes', 'Glúteos'], hamstrings: ['Hamstrings', 'Isquiotibiales'],
  calves: ['Calves', 'Pantorrillas'], erectors: ['Spinal erectors', 'Erectores espinales'], chest: ['Chest', 'Pecho'],
  shoulders: ['Shoulders', 'Hombros'], upper_back: ['Upper back', 'Espalda alta'], lats: ['Lats', 'Dorsales'],
  biceps: ['Biceps', 'Bíceps'], triceps: ['Triceps', 'Tríceps'], forearms: ['Forearms', 'Antebrazos'], core: ['Core', 'Zona media'],
  dumbbells: ['Dumbbells', 'Mancuernas'], bench: ['Bench', 'Banco'], step: ['Stable step', 'Escalón estable'], mat: ['Mat', 'Colchoneta'],
  cable_machine: ['Cable machine', 'Poleas'], barbell: ['Barbell', 'Barra'],
  beginner: ['Beginner', 'Principiante'], intermediate: ['Intermediate', 'Intermedio'], advanced: ['Advanced', 'Avanzado'],
  general_fitness: ['General fitness', 'Condición física'], strength: ['Strength', 'Fuerza'], hypertrophy: ['Hypertrophy', 'Hipertrofia'],
};
export const label = (key: string, language: Language) => labels[key]?.[language === 'en' ? 0 : 1] ?? key;
export const names = (keys: string[], language: Language) => keys.map(key => label(key, language)).join(' · ');
export const t = (language: Language, en: string, es: string) => language === 'en' ? en : es;
