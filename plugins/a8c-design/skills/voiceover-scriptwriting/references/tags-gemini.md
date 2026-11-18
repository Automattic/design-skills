# Tag dictionary — Gemini 3.8 Flash TTS

Gemini TTS treats the text field as a **verbatim transcript** — it will read anything in it aloud. Direction is split across two scopes:

1. **Sustained (turn-level) delivery** → the `speech_metadata.style` field.
2. **Momentary vocal events** → inline angle-bracket tags. **Human vocalizations only — never sound-effect tags.**

## Inline vocalization tags

`<argh>` `<breath>` `<heavy breath>` `<exhales>` `<cackle>` `<cheer>` `<chuckle>` / `<chuckles>` `<cough>` `<cry>` `<gasp>` `<giggle>` `<groan>` `<growl>` `<grunt>` `<grr>` `<hiss>` `<laugh>` / `<laughter>` `<moan>` `<pant>` `<pff>` / `<phew>` `<scream>` `<shout>` `<shriek>` `<sigh>` / `<sighs>` `<sneeze>` `<snicker>` `<snort>` `<sob>` `<throat-clearing>` `<tsk>` `<whimper>` `<whispers>` / `<whispering>` `<yawn>`

Pauses: `<short pause>` `<long pause>`

```
"Wait... <short pause> did you hear that? <sigh>"
"Excuse me <cough> as I was saying..."
```

For non-English transcripts, keep the inline tags in English.

## The style field (`speech_metadata.style`)

Short strings, reused verbatim for consistency:

`"cheerful and friendly"` · `"calm and relaxed"` · `"whispered urgently"` · `"warm and enthusiastic"` · `"out of breath"` · `"muttering"` · `"sarcastic"` · `"angry tone"` · `"speaking rapidly"` · `"speaking slowly"` · `"monotone and flat"` · `"high pitch, cheerful and excited inflection"`

If emotion changes mid-piece, **split into separate turns** with a different `style` per turn — don't embed the shift in the text.

## Three levels of pacing control

1. **Punctuation:** commas, `--`, `...` for natural hesitations.
2. **Inline tags:** `<short pause>` / `<long pause>` at exact positions.
3. **Turn-level style:** `"speaking rapidly"` / `"speaking slowly"`.

## Emphasis

Capitalize the key word in the transcript, combined with punctuation and inline vocalization tags:

```
"This is a VERY important point!"
"It was a VERY long day <sigh> ... nobody listens anymore."
```

## Backchannels and overlapping speech (`|...|`)

Place a listener's reaction inside pipe characters within the speaker's turn:

- Short exchange: `"So the launch is Thursday |oh hmm| Are we actually ready?"`
- Simultaneous: `"Let's surprise him on three |ok| ready?"` then `"one. two. three. |happy| happy |birthday| birthday!"`

## Anti-drift rules (the most common failure causes)

- **Test plain TTS with an empty style field first.** Most requests need no style at all.
- Add only short style strings and **reuse the exact same string** for a consistent baseline.
- **Never embed meta-instructions** ("maintain identical timbre", "do not switch speaker identity") or long "Audio Profile" / "Director's Notes" paragraphs — these *increase* voice drift.
- Immutable traits (age, gender, permanent accent) belong in **voice selection**, not the style field. Use a persistent `voice_...` ID from Voice Design for a custom persona.
- Multi-turn agents: one TTS call per turn, identity carried by the configured voice; split long answers into shorter turns rather than stronger style.

## Multi-speaker requests

Always set the `speaker` field in `speech_metadata` — it must match a configured speaker. Unmatched speakers fail or drift.
