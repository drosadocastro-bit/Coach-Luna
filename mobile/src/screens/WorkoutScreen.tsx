import { Text, View } from 'react-native';
import { ExerciseCard } from '../components/ExerciseCard';
import { WorkoutHeader } from '../components/WorkoutHeader';
import { Button, styles } from '../components/ui';
import { Language } from '../types/exercise';
import { RoutineRequest, RoutineResponse } from '../types/routine';
import { t } from '../i18n';

export function WorkoutScreen({ language, response, request, completed, onComplete, onView, onBack }: {
  language: Language; response: RoutineResponse; request: RoutineRequest; completed: Set<string>;
  onComplete: (id: string) => void; onView: (id: string) => void; onBack: () => void;
}) {
  return <>
    <Button title={t(language, 'New workout', 'Nuevo entrenamiento')} onPress={onBack} />
    <WorkoutHeader language={language} targets={request.target_muscles} duration={response.routine.estimated_duration_minutes} completed={completed.size} count={response.routine.exercises.length} />
    {response.validation.warnings.length > 0 && <View style={styles.card}><Text style={styles.muted}>{t(language, 'This first version uses the same catalog sets and reps for every goal. Timing includes estimated rest.', 'Esta primera versión usa las mismas series y repeticiones del catálogo para cada objetivo. El tiempo incluye descanso estimado.')}</Text>
      {response.routine.estimated_duration_minutes > request.duration_minutes && <Text style={styles.body}>{t(language, 'This workout may exceed your selected duration. Reduce the exercise count or allow more time.', 'Este entrenamiento puede superar la duración elegida. Reduce la cantidad de ejercicios o reserva más tiempo.')}</Text>}
      {response.validation.warnings.some(w => w.includes('movement pattern')) && <Text style={styles.muted}>{t(language, 'Several exercises share a movement pattern.', 'Varios ejercicios comparten un patrón de movimiento.')}</Text>}
    </View>}
    {response.routine.exercises.map(item => <ExerciseCard key={item.exercise_id} item={item} language={language} complete={completed.has(item.exercise_id)} onComplete={() => onComplete(item.exercise_id)} onView={() => onView(item.exercise_id)} />)}
  </>;
}
