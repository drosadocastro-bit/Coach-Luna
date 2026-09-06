import { Text, View } from 'react-native';
import { Language } from '../types/exercise';
import { RoutineItem } from '../types/routine';
import { names, t } from '../i18n';
import { Button, styles } from './ui';
import { VideoPlaceholder } from './VideoPlaceholder';

export function prescription(item: Pick<RoutineItem, 'sets' | 'rep_min' | 'rep_max'>, unit: string, unilateral: boolean, language: Language) {
  return `${item.sets} × ${item.rep_min}–${item.rep_max} ${unit === 'steps' ? t(language, 'steps', 'pasos') : t(language, 'reps', 'repeticiones')}${unilateral ? t(language, ' / side', ' / lado') : ''}`;
}

export function ExerciseCard({ item, language, complete, onView, onComplete }: { item: RoutineItem; language: Language; complete: boolean; onView: () => void; onComplete: () => void }) {
  return <View style={styles.card}>
    <Text style={styles.heading}>{language === 'en' ? item.exercise.name : item.exercise.display_name_es}</Text>
    <Text style={styles.body}>{prescription(item, item.exercise.prescription_unit, item.exercise.unilateral, language)}</Text>
    <Text style={styles.muted}>{names(item.exercise.primary_muscles, language)}</Text>
    <Text style={styles.muted}>{names(item.exercise.equipment, language)}</Text>
    <VideoPlaceholder language={language} />
    <Button title={t(language, 'View Exercise', 'Ver ejercicio')} onPress={onView} />
    <Button title={complete ? t(language, 'Completed · Undo', 'Completado · Deshacer') : t(language, 'Complete', 'Completar')} onPress={onComplete} />
  </View>;
}
