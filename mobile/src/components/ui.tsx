import { Pressable, StyleSheet, Text, View } from 'react-native';

export const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: '#F7F5F0' },
  page: { padding: 24, paddingBottom: 48, width: '100%', maxWidth: 680, alignSelf: 'center', gap: 20 },
  title: { fontSize: 34, fontWeight: '700', color: '#243E36', letterSpacing: -1 },
  heading: { fontSize: 21, fontWeight: '600', color: '#243E36' },
  body: { fontSize: 16, lineHeight: 24, color: '#485B53' },
  muted: { fontSize: 13, lineHeight: 20, color: '#576B62' },
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, alignItems: 'center' },
  card: { backgroundColor: '#FFFFFF', borderRadius: 20, padding: 20, gap: 12, borderColor: '#DEE5DD', borderWidth: 1 },
  button: { backgroundColor: '#315C49', paddingHorizontal: 20, paddingVertical: 15, borderRadius: 14, alignItems: 'center', minHeight: 48 },
  buttonText: { color: '#FFFFFF', fontWeight: '600', fontSize: 16 },
  chip: { paddingHorizontal: 14, paddingVertical: 12, borderRadius: 12, backgroundColor: '#E9EEE7', minHeight: 44 },
  selected: { backgroundColor: '#315C49' },
  chipText: { color: '#315C49', fontSize: 14 },
  error: { backgroundColor: '#F8E6DF', padding: 16, borderRadius: 12 },
});

export function Button({ title, onPress, disabled = false }: { title: string; onPress: () => void; disabled?: boolean }) {
  return <Pressable accessibilityRole="button" accessibilityState={{ disabled }} disabled={disabled} onPress={onPress} style={[styles.button, disabled && { opacity: 0.5 }]}><Text style={styles.buttonText}>{title}</Text></Pressable>;
}

export function Choices<T extends string | number>({ values, selected, onSelect, display }: {
  values: readonly T[]; selected: readonly T[]; onSelect: (value: T) => void; display: (value: T) => string;
}) {
  return <View style={styles.row}>{values.map(value => <Pressable key={value} accessibilityRole="button" accessibilityState={{ selected: selected.includes(value) }} onPress={() => onSelect(value)} style={[styles.chip, selected.includes(value) && styles.selected]}><Text style={[styles.chipText, selected.includes(value) && { color: '#FFFFFF' }]}>{display(value)}</Text></Pressable>)}</View>;
}
