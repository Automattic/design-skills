# Advanced techniques — cloning, mixing, pipelines, and native-audio video

Load when generating audio end-to-end, mixing, working with clones, or steering native-audio video generators.

## Separating performance from identity

Emotional delivery (timing, rhythm, energy) and voice identity (timbre, formants) are **separable**. Pipeline: render the performance with an expressive model, then pass the audio through ElevenLabs' Voice Changer to swap in the brand clone while preserving timing, emphasis, pauses, and breaths. Useful when a clone can't hit an emotional peak directly.

## Clone quality and stability

- Source quality decides everything: voices trained on recordings with **natural emotional variety** respond to emotion tags; flat/monotone source recordings produce flat clones that ignore tags.
- Instant Voice Clones (IVC) capture a voice from as little as 10 seconds of audio, but 1–2 minutes is recommended. Professional Voice Clones (PVC) give noticeably better identity matching for production use.
- Clones made on older models need retraining for v4.
- Pushing a clone's similarity setting too high introduces artifacts: inconsistent speed, mispronunciation, random volume changes.
- Creative mode has the most expressive range but can hallucinate sounds; **Natural mode is the safe default** for brand work.

## Per-scene pipeline (Claude Code + ElevenLabs + FFmpeg pattern)

- `script.json` is the single source of truth — one entry per scene: `scene_id`, `duration`, `narration`, `visual_description`.
- **One TTS call per scene.** Editing a line means regenerating only that scene — every layer stays independently adjustable and idempotent.
- Build a **10–15% buffer** into each scene's duration: TTS does not guarantee narration fits the scene. Use FFmpeg's `-shortest` flag when combining to avoid silent gaps.
- Validate narration length per scene with `scripts/check_duration.py --json script.json` before generating audio.
- A 60-second, six-scene job typically costs under $1 in TTS — cheap enough to iterate.

## Mixing and audio targets

- Music under narration: mix at ~20% volume (e.g. FFmpeg `amix`). Lyric-heavy music makes 180-WPM narration hard to follow.
- Gain staging: loudest peaks around −12 to −6 dB; record at 24-bit/48kHz.
- Loudness is measured in LUFS: ~−16 LUFS is a common podcast target.
- ACX audiobook specs (if relevant): averages −23 to −18 dB, peaks no higher than −3 dB.
- Always leave the editor buffer time — a 15-second placement should not require exactly 15.00 seconds of uninterrupted speech.

## Consent, disclosure, and provenance

- SAG-AFTRA's Interactive Media Agreement (ratified July 2025): clear consent and disclosure before a performer's voice is replicated, compensation linked to use — its terms are becoming a market baseline even outside union work.
- EU AI Act Article 50: a synthetic voice resembling a real person is a "deepfake" regardless of consent; disclosure failures risk fines up to €15M or 3% of worldwide turnover. Conversational AI must identify itself as artificial unless obvious from context.
- Provenance watermarking is shipping (e.g. SynthID on Gemini TTS output) — check your provider's policy before stripping metadata.
- Granular opt-in consent for vocal biometrics is the ethics baseline; on Apple platforms, Personal Voice access is governed by the user's authorization (`personalVoiceAuthorizationStatus`, iOS 17+/macOS 14+).

## Native audio in video generators

- **Sora 2** (Sept 2026): generates up to 25s with synchronized audio — lip-synced dialogue, ambience, music — and can regenerate only the audio track. Known limitation on realistic identifiable humans. Steering is prompt-based: describe dialogue timing and specify ambient/music ("Ambient coffee shop sounds and soft indie music play in the background").
- **Veo 3.1**: native audio (SFX, ambience, dialogue) generated alongside video.
- **Inworld, Minimax, Seedance** and similar increasingly include audio directly and steer via reference — the same rule applies: vendor-specific guidance, vendor-specific tags.

## Emotion-aware delivery notes

- Think in valence / arousal / dominance rather than discrete labels when a read feels "off" — name the axes you want moved.
- Prosodic micro-behaviors: ~150–300ms pauses when delivering bad news; word-level dynamic range for emphasis.
- Empathy is cultural: high-pitch/high-energy reads as warmth in Western contexts but insincere in much of East Asia; in tonal languages, emotional pitch shifts must not disrupt word meaning.
- The 2026 shift: from rule-based tone control (manual SSML, static pitch/speed) to context-aware synthesis adapting prosody, micro-pauses, breaths, and vocal tremor to meaning — write scripts that *carry* their direction so one generation pass gets the expressive result.
