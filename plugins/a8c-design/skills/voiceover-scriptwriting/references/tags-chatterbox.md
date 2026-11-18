# Tag dictionary — Chatterbox (open source, Resemble AI)

Chatterbox is MIT-licensed TTS with zero-shot voice cloning from a reference clip — a common FOSS default. Control is **mostly parametric**; inline paralinguistic tags exist only on Turbo-class models.

## Original / Multilingual models — parameter control

- `exaggeration`: expressive intensity. Defaults ~0.5; higher values (≈0.7+) are more dramatic but speed the speech up — compensate with pacing in the script.
- `cfg_weight`: pacing control. Lower to ~0.3 for expressive reads, or to compensate for a fast-talking reference speaker.
- `language_id`: selects the language (multilingual model).
- No inline emotion tags: encode emotion in the script's wording and punctuation, and let the parameters shape delivery.

## Turbo / Nano — inline paralinguistic tags

`[laugh]` `[chuckle]` `[cough]` and similar paralinguistic tags are native to the Turbo model family; place them inline where the vocalization should occur.

- **Turbo** (350M): low-latency, English.
- **Nano** (110M): CPU/on-device, runs ~3× realtime on 8 cores — the pick for local or embedded pipelines.
- **Multilingual V3** (500M): 23+ languages, improved speaker similarity.

## Notes

- Cloning quality follows the same rule as everywhere else: expressive, natural source audio in, expressive response to control out; flat references produce flat output.
- No SSML. For pauses, use punctuation and line breaks; for emphasis, reword the sentence.
