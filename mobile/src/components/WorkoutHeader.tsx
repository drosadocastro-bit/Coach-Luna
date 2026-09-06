import { Text, View } from 'react-native';
import { Language, Muscle } from '../types/exercise';
import { names, t } from '../i18n';
import { styles } from './ui';

export function WorkoutHeader({ language, targets, duration, completed, count }: { language: Language; targets: Muscle[]; duration: number; completed: number; count: number }) {
  return <View style={{ gap: 10 }}>
    <Text style={styles.title}>{names(targets, language)}</Text>
    <Text style={styles.body}>{t(language, 'Your workout, one step at a time.', 'Tu entrenamiento, paso a paso.')}</Text>
    <Text style={styles.muted}>{duration} min {t(language, 'estimated', 'estimados')} · {completed}/{count} {t(language, 'marked complete', 'marcados como completados')}</Text>
    <Text style={styles.muted}>{t(language, 'Completion marks stay in this session only.', 'Las marcas se conservan solo durante esta sesión.')}</Text>
  </View>;
}
