import { useEffect, useState } from 'react';
import { BackHandler, ScrollView, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { coachLunaApi } from './src/api/coachLunaApi';
import { Choices, styles } from './src/components/ui';
import { Language } from './src/types/exercise';
import { RoutineRequest, RoutineResponse } from './src/types/routine';
import { HomeScreen } from './src/screens/HomeScreen';
import { WorkoutScreen } from './src/screens/WorkoutScreen';
import { ExerciseScreen } from './src/screens/ExerciseScreen';

export default function App() {
  const [language, setLanguage] = useState<Language>('en');
  const [screen, setScreen] = useState<'home' | 'workout' | 'exercise'>('home');
  const [workout, setWorkout] = useState<{ request: RoutineRequest; response: RoutineResponse } | null>(null);
  const [exerciseId, setExerciseId] = useState('');
  const [completed, setCompleted] = useState<Set<string>>(new Set());
  useEffect(() => {
    const subscription = BackHandler.addEventListener('hardwareBackPress', () => {
      if (screen === 'home') return false;
      setScreen(screen === 'exercise' ? 'workout' : 'home');
      return true;
    });
    return () => subscription.remove();
  }, [screen]);
  async function generate(request: RoutineRequest) {
    const response = await coachLunaApi.generate(request);
    setWorkout({ request, response }); setCompleted(new Set()); setScreen('workout');
  }
  function viewExercise(id: string) { setExerciseId(id); setScreen('exercise'); }
  function toggleComplete(id: string) {
    setCompleted(previous => { const next = new Set(previous); next.has(id) ? next.delete(id) : next.add(id); return next; });
  }
  return <SafeAreaProvider><SafeAreaView style={styles.safe}>
    <StatusBar style="dark" />
    <ScrollView key={`${screen}:${screen === 'exercise' ? exerciseId : ''}`} contentContainerStyle={styles.page}>
      <View style={{ alignItems: 'flex-end' }}><Choices<Language> values={['en', 'es']} selected={[language]} onSelect={setLanguage} display={value => value === 'en' ? 'English' : 'Español'} /></View>
      {screen === 'home' && <HomeScreen language={language} onGenerate={generate} />}
      {screen === 'workout' && workout && <WorkoutScreen language={language} {...workout} completed={completed} onComplete={toggleComplete} onView={viewExercise} onBack={() => setScreen('home')} />}
      {screen === 'exercise' && <ExerciseScreen id={exerciseId} language={language} onBack={() => setScreen('workout')} onView={viewExercise} />}
    </ScrollView>
  </SafeAreaView></SafeAreaProvider>;
}
