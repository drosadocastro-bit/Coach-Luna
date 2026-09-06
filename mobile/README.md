# Mobile

Expo SDK 57, React Native, TypeScript. The blank TypeScript template avoids unused routing dependencies; `App.tsx` owns navigation, language, current workout and session completion state. Screen components live under `src/screens` and use the shared typed API client.

```powershell
cd D:\CoachLuna\mobile
npm.cmd ci
Copy-Item .env.example .env
# Set EXPO_PUBLIC_API_URL for the test device, then:
npm.cmd start
```

Use Expo Go compatible with SDK 57 on iPhone/Android, or an Android emulator. A Windows host cannot launch an iOS simulator. A separate Mac is needed for local iOS builds. Check the SDK compatibility at [Expo Go](https://expo.dev/go).

```powershell
npm.cmd run web
npm.cmd run typecheck
npx.cmd expo install --check
npm.cmd run export
```

The API defaults to `http://localhost:8000` for browser testing. For phones use the Windows LAN address in `.env` and restart Metro; see [networking](../docs/LOCAL_NETWORKING.md). Never place provider keys in `EXPO_PUBLIC_*`: those values are embedded in bundles.

Flow: choose language, focus, duration, equipment, experience, goal and count; generate; view cards; mark an exercise complete; open details and browse alternatives. Completion resets with app reload or a new workout. Alternatives are informational and never silently replace a validated exercise. English and Spanish strings are local, with no translation service. Loading, timeout, retry and infeasible-request states are included.

The standard Expo template icons are temporary. No demonstration media or real playback is bundled. Web testing covers shared screen behavior but cannot establish native-device networking or rendering correctness; native checks are tracked in verification notes.
