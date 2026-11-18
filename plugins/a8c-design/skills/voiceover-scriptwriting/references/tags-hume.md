# Tag dictionary — Hume (Octave)

Octave is steered with **natural-language acting instructions**, not a fixed tag set. Emotion and delivery go in the utterance-level `description` field; only pause markers live inside the text.

## Acting instructions (`description` field, per utterance)

Short phrases — keep under ~100 characters; precise beats broad:

- `"whispering, hushed"` · `"urgent, panicked"` · `"warm, inviting"` · `"sarcastic"` · `"calm, pedagogical"`
- Combine emotion + style: `"excited but whispering"`, `"confident, professional tone"`.
- Name the audience: `"speaking to a child"` shapes delivery.
- Prefer precise emotions ("melancholy", "frustrated") over broad ones ("sad").

## Rate and silence (parameters, not words)

- `speed`: 0.5 (slower) – 2.0 (faster), 1.0 = normal, non-linear scale. Don't put rate in the description — use the parameter.
- `trailing_silence`: seconds of silence appended after an utterance — useful for beats between scenes.

## Inline text markers

`[pause]` and `[long pause]` go inside the text where the beat should land:

```
"Haha [pause] I didn't realize this was going to be a formal event."
```

## Notes

- Per Hume's docs, the `description` field is supported on Octave 1, with Octave 2 support listed as coming soon — check the current API before relying on it for Octave 2, and otherwise steer Octave 2 through voice choice and the speed parameter.
- If no voice is specified, `description` doubles as a voice-design prompt — always pair a description with an explicit voice.
