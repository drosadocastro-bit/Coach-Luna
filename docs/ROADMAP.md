# Roadmap

## Phase 0 — Repository + deterministic vertical slice

Typed catalog, SQLite bootstrap, deterministic engine, independent validator, FastAPI endpoints, tests, bilingual Expo screens, local setup and verification. Physical-device verification remains a separate gate when hardware is available.

## Phase 1 — Exercise media integration

Select owned/licensed media; record permission and attribution; review form and bilingual cues; prepare 5–15 second MP4 loops with appropriate angles; map each asset to an exercise ID; add local playback and loading/error/offline behavior; verify on iOS and Android. No production hosting is assumed.

## Phase 2 — Natural-language prompt parsing with OpenAI

Implement a backend intent adapter with verified provider/model availability, strict request parsing and bounded deterministic selection. The proposed model name is planning input, not a Phase 0 integration or availability claim.

## Phase 3 — Coach Luna voice using ElevenLabs

Backend TTS adapter, female bilingual voice selection, permissions, caching and failure handling. Keep identity provider-independent.

## Phase 4 — Workout history and progression

Persist user-confirmed sessions and design transparent progression rules. Add database migrations before history becomes durable product data.

## Phase 5 — Exercise replacement and equipment occupied behavior

Use catalog alternatives, recheck equipment/experience and validate the revised workout.

## Phase 6 — Private iOS/Android distribution and real-world testing

Private builds, device compatibility, accessibility, networking and gym testing with explicit feedback.
