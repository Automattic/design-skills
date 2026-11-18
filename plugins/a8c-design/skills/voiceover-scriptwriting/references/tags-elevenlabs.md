# Tag dictionary — ElevenLabs (v3 / v4)

ElevenLabs models are directed through **inline square-bracket tags** plus punctuation. **SSML is not supported** — tags and punctuation do all the work v3/v4 need. The model reads tags as performance direction, not words to speak.

## Emotion

`[sad]` `[angry]` `[happily]` `[sorrowful]` `[excited]` `[worried]` `[awed]` `[softly]` `[dismissive]` `[cheeky]` `[annoyed]` `[surprised]`

Example: `[sorrowful] I couldn't sleep that night.`

## Delivery & pacing

- `[whispers]` `[shouts]` `[softly]` — volume and energy
- `[rushed]` — fast delivery; `[drawn out]` or `[slowly]` — slow delivery
- `[pause]` — a deliberate beat (the SSML `<break>` equivalent)

## Human reactions

`[laughs]` `[big laugh]` `[chuckles]` `[sighs]` `[sighing]` `[clears throat]` `[coughing]` `[gasps]`

## Dialogue & interaction (multi-voice scenes)

`[jumping in]` `[interrupting]` `[overlapping]` `[beginning to speak]` `[cautiously]` `[panicking]` — start each dialogue line with a tag.

## Accents & characters

`[French accent]` `[australian accent]` `[British accent]` `[pirate voice]` — shift voice without switching models.

## Sound effects

`[gunshot]` `[explosion]` `[clapping]` `[light rain]` `[phone buzzing]` — non-speech audio generated inline. Use sparingly in narration; a dedicated sound-effects generator gives more control.

## Combining and layering

Multiple tags can appear in one sentence for a layered performance:

```
[tired] It's been a long day… [upset] How many more days can I take?
```

## Punctuation as prosody

| Punctuation | Effect |
|---|---|
| Ellipsis `…` | natural pause |
| Line break | longer beat |
| Comma | breathing rhythm |
| Period | cut |
| Em dash | dramatic beat |
| ALL CAPS | emphasis ("I want it right NOW.") |

## Placement, limits, and failure modes

- Place tags anywhere in the script to shape delivery in real time; they work identically in the UI and the API, and with Instant and Professional Voice Clones.
- **Tags occasionally get spoken aloud as literal text.** This happens when the voice doesn't suit the requested delivery — e.g. a soft-spoken voice asked for repeated `[shouts]`. Fix: pick a wide-emotional-range voice, confirm the model is set to the latest version.
- **Tag peaks, not every line.** Over-tagging produces audio that shifts register sentence by sentence; cloned voices trained on flat recordings tend to ignore emotion tags entirely.
- v4 follows sequences of tags (two directions in one line) more reliably than v3, and adds phonetic (IPA) pronunciation control for tricky words.
- Expressiveness trades against stability. Pushing a clone's similarity setting too high introduces artifacts: uneven speed, mispronunciation, random volume changes. Natural mode is the safe default for brand work; Creative mode has the widest range but can hallucinate sounds.
- Intentional pauses (`[pause]`, ellipses) still consume scene time — count them in the duration check.
