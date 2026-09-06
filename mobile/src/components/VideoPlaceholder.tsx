import { Text, View } from 'react-native';
import { Language } from '../types/exercise';
import { t } from '../i18n';
import { styles } from './ui';

export function VideoPlaceholder({ language }: { language: Language }) {
  return <View style={{ backgroundColor: '#EAF0E8', borderRadius: 14, padding: 24, minHeight: 105, justifyContent: 'center', alignItems: 'center', gap: 6 }}>
    <Text style={{ fontSize: 24, color: '#55775D' }}>▷</Text>
    <Text style={styles.muted}>{t(language, 'Exercise demonstration coming soon', 'Demostración del ejercicio próximamente')}</Text>
  </View>;
}
