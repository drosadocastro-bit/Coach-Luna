import { useEffect, useState } from 'react';
import { ActivityIndicator, Text, View } from 'react-native';
import { useVideoPlayer, VideoView } from 'expo-video';
import { coachLunaApi } from '../api/coachLunaApi';
import { Language } from '../types/exercise';
import { MediaVideo } from '../types/media';
import { Choices, styles } from './ui';

function ReadyVideo({ video }: { video: MediaVideo }) {
  const player = useVideoPlayer(video.url, p => { p.loop = true; p.muted = true; p.play(); });
  return <VideoView player={player} style={{ width: '100%', aspectRatio: 16 / 9, borderRadius: 16, overflow: 'hidden' }} contentFit="contain" nativeControls={false} />;
}

export function ExerciseVideo({ exerciseId, language, preferredAngle }: { exerciseId: string; language: Language; preferredAngle?: string }) {
  const [video, setVideo] = useState<MediaVideo | null>(null);
  const [angles, setAngles] = useState<string[]>([]);
  const [selected, setSelected] = useState(preferredAngle || '');
  const [loading, setLoading] = useState(true);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    let active = true;
    setLoading(true); setFailed(false);
    coachLunaApi.media(exerciseId, selected || preferredAngle).then(response => {
      if (!active) return;
      const next = response.canonical;
      setVideo(next); setAngles(next?.available_angles || []);
      if (next) setSelected(next.angle);
      setLoading(false);
    }).catch(() => { if (active) { setVideo(null); setLoading(false); setFailed(true); } });
    return () => { active = false; };
  }, [exerciseId, selected, preferredAngle]);
  if (loading) return <View style={styles.card}><ActivityIndicator color="#315C49" /><Text style={styles.muted}>{language === 'en' ? 'Loading demonstration…' : 'Cargando demostración…'}</Text></View>;
  if (failed || !video) return <View style={styles.card}><Text style={styles.muted}>{language === 'en' ? 'Demonstration unavailable' : 'Demostración no disponible'}</Text></View>;
  return <View style={styles.card}><ReadyVideo video={video} />{angles.length > 1 && <Choices values={angles} selected={[selected]} onSelect={setSelected} display={angle => angle.replace('_', ' ')} />}</View>;
}
