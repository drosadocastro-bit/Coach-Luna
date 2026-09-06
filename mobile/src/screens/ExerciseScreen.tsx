import { useEffect, useState } from 'react';
import { ActivityIndicator, Text, View } from 'react-native';
import { coachLunaApi } from '../api/coachLunaApi';
import { prescription } from '../components/ExerciseCard';
import { VideoPlaceholder } from '../components/VideoPlaceholder';
import { Button, styles } from '../components/ui';
import { names, t } from '../i18n';
import { Exercise, Language } from '../types/exercise';

export function ExerciseScreen({ id, language, onBack, onView }: { id: string; language: Language; onBack: () => void; onView: (id: string) => void }) {
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [alternatives, setAlternatives] = useState<Exercise[]>([]);
  const [error, setError] = useState(false);
  const [alternativeError, setAlternativeError] = useState(false);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let active = true;
    setExercise(null); setAlternatives([]); setError(false); setAlternativeError(false);
    coachLunaApi.exercise(id).then(async value => {
      if (!active) return;
      setExercise(value);
      const results = await Promise.allSettled(value.alternatives.map(coachLunaApi.exercise));
      if (active) {
        setAlternatives(results.flatMap(result => result.status === 'fulfilled' ? [result.value] : []));
        setAlternativeError(results.some(result => result.status === 'rejected'));
      }
    }).catch(() => { if (active) setError(true); });
    return () => { active = false; };
  }, [id, attempt]);
  return <>
    <Button title={t(language, 'Back to workout', 'Volver al entrenamiento')} onPress={onBack} />
    {error ? <View style={styles.error}><Text style={styles.body}>{t(language, 'Could not load this exercise.', 'No se pudo cargar este ejercicio.')}</Text><Button title={t(language, 'Retry', 'Reintentar')} onPress={() => setAttempt(a => a + 1)} /></View> : !exercise ? <ActivityIndicator color="#315C49" /> : <>
      <Text style={styles.title}>{language === 'en' ? exercise.name : exercise.display_name_es}</Text>
      <VideoPlaceholder language={language} />
      <Text style={styles.body}>{prescription({ sets: exercise.default_sets, rep_min: exercise.rep_min, rep_max: exercise.rep_max }, exercise.prescription_unit, exercise.unilateral, language)}</Text>
      <Text style={styles.heading}>{t(language, 'Primary muscles', 'Músculos principales')}</Text><Text style={styles.body}>{names(exercise.primary_muscles, language)}</Text>
      <Text style={styles.heading}>{t(language, 'Secondary muscles', 'Músculos secundarios')}</Text><Text style={styles.body}>{names(exercise.secondary_muscles, language) || t(language, 'None listed', 'Ninguno indicado')}</Text>
      <Text style={styles.heading}>{t(language, 'Equipment', 'Equipo')}</Text><Text style={styles.body}>{names(exercise.equipment, language)}</Text>
      <Text style={styles.heading}>{t(language, 'How to move', 'Cómo realizarlo')}</Text>
      {(language === 'en' ? exercise.instructions_en : exercise.instructions_es).map((cue, i) => <Text key={i} style={styles.body}>{i + 1}. {cue}</Text>)}
      <Text style={styles.heading}>{t(language, 'Common mistakes', 'Errores comunes')}</Text>
      {(language === 'en' ? exercise.common_mistakes_en : exercise.common_mistakes_es).map((cue, i) => <Text key={i} style={styles.body}>• {cue}</Text>)}
      <Text style={styles.heading}>{t(language, 'Alternatives', 'Alternativas')}</Text>
      <Text style={styles.muted}>{t(language, 'Browse only. Alternatives may need different equipment or experience; they do not replace your workout automatically.', 'Solo para consultar. Pueden requerir otro equipo o experiencia; no sustituyen automáticamente tu entrenamiento.')}</Text>
      {alternatives.map(alt => <Button key={alt.id} title={language === 'en' ? alt.name : alt.display_name_es} onPress={() => onView(alt.id)} />)}
      {alternativeError && <Text style={styles.muted}>{t(language, 'Some alternatives could not be loaded.', 'No se pudieron cargar algunas alternativas.')}</Text>}
    </>}
  </>;
}
