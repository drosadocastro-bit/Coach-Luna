import { useState } from 'react';
import { ActivityIndicator, Text, View } from 'react-native';
import { ApiError } from '../api/coachLunaApi';
import { Button, Choices, styles } from '../components/ui';
import { label, t } from '../i18n';
import { Equipment, Language, Muscle } from '../types/exercise';
import { RoutineRequest } from '../types/routine';

const focuses: { en: string; es: string; muscles: Muscle[] }[] = [
  { en: 'Glutes + hamstrings', es: 'Glúteos + isquiotibiales', muscles: ['glutes', 'hamstrings'] },
  { en: 'Legs', es: 'Piernas', muscles: ['quads', 'glutes'] },
  { en: 'Upper body', es: 'Tren superior', muscles: ['chest', 'lats', 'shoulders'] },
  { en: 'Full body', es: 'Cuerpo completo', muscles: ['quads', 'chest', 'lats'] },
  { en: 'Core', es: 'Zona media', muscles: ['core'] },
];

export function HomeScreen({ language, onGenerate }: { language: Language; onGenerate: (request: RoutineRequest) => Promise<void> }) {
  const [focus, setFocus] = useState(0);
  const [duration, setDuration] = useState(45);
  const [equipment, setEquipment] = useState<Equipment[]>(['dumbbells', 'bench']);
  const [level, setLevel] = useState<RoutineRequest['experience_level']>('beginner');
  const [goal, setGoal] = useState<RoutineRequest['goal']>('general_fitness');
  const [count, setCount] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<'request' | 'network' | 'server' | null>(null);
  async function generate() {
    setLoading(true); setError(null);
    try { await onGenerate({ target_muscles: focuses[focus].muscles, duration_minutes: duration, equipment, experience_level: level, goal, exercise_count: count }); }
    catch (failure) { setError(failure instanceof ApiError ? failure.kind : 'server'); }
    finally { setLoading(false); }
  }
  return <>
    <View style={{ gap: 12 }}><Text style={styles.muted}>{t(language, 'A LITTLE MOVEMENT. YOUR OWN PACE.', 'UN POCO DE MOVIMIENTO. A TU RITMO.')}</Text><Text style={styles.title}>Coach Luna</Text><Text style={styles.body}>{t(language, 'Your warm, grounded bilingual fitness coach.', 'Tu entrenadora bilingüe, cercana y con los pies en la tierra.')}</Text></View>
    <View style={styles.card}>
      <Text style={styles.heading}>{t(language, 'Make room for yourself', 'Un momento para ti')}</Text>
      <Text style={styles.body}>{t(language, 'Choose your focus and what you have available. We’ll build from there.', 'Elige tu enfoque y el equipo disponible. Empezamos desde ahí.')}</Text>
    </View>
    <Text style={styles.heading}>{t(language, 'Workout focus', 'Enfoque')}</Text>
    <Choices values={[0, 1, 2, 3, 4]} selected={[focus]} onSelect={setFocus} display={i => focuses[i][language]} />
    <Text style={styles.heading}>{t(language, 'Duration', 'Duración')}</Text>
    <Choices values={[20, 30, 45, 60]} selected={[duration]} onSelect={setDuration} display={n => `${n} min`} />
    <Text style={styles.heading}>{t(language, 'Available equipment', 'Equipo disponible')}</Text>
    <Choices<Equipment> values={['dumbbells', 'bench', 'step', 'mat']} selected={equipment} display={value => label(value, language)} onSelect={value => setEquipment(old => old.includes(value) ? old.filter(e => e !== value) : [...old, value])} />
    <Text style={styles.muted}>{t(language, 'Incline exercises need an adjustable bench. Floor work can use an optional mat.', 'Los ejercicios inclinados necesitan un banco regulable. La colchoneta es opcional para el suelo.')}</Text>
    <Text style={styles.heading}>{t(language, 'Experience level', 'Experiencia')}</Text>
    <Choices<RoutineRequest['experience_level']> values={['beginner', 'intermediate', 'advanced']} selected={[level]} onSelect={setLevel} display={value => label(value, language)} />
    <Text style={styles.heading}>{t(language, 'Goal', 'Objetivo')}</Text>
    <Choices<RoutineRequest['goal']> values={['general_fitness', 'strength', 'hypertrophy']} selected={[goal]} onSelect={setGoal} display={value => label(value, language)} />
    <Text style={styles.heading}>{t(language, 'Exercise count', 'Cantidad de ejercicios')}</Text>
    <Choices values={[3, 4, 5, 6]} selected={[count]} onSelect={setCount} display={String} />
    {error && <View accessibilityRole="alert" style={styles.error}><Text style={styles.body}>{error === 'request' ? t(language, 'This combination cannot cover your focus. Try adding equipment or changing the focus or exercise count.', 'Esta combinación no cubre tu enfoque. Prueba añadir equipo o cambiar el enfoque o la cantidad de ejercicios.') : error === 'network' ? t(language, 'We couldn’t reach the backend. Check your connection and try again.', 'No pudimos conectar con el servidor. Revisa la conexión e inténtalo de nuevo.') : t(language, 'The workout is unavailable right now. Please try again.', 'El entrenamiento no está disponible ahora. Inténtalo de nuevo.')}</Text></View>}
    {loading && <ActivityIndicator color="#315C49" />}
    <Button disabled={loading || !equipment.length} title={loading ? t(language, 'Building your workout…', 'Preparando tu entrenamiento…') : t(language, 'Generate Workout', 'Generar entrenamiento')} onPress={generate} />
  </>;
}
