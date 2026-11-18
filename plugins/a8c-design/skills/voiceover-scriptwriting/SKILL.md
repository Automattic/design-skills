---
name: voiceover-scriptwriting
description: Writes polished voiceover scripts for AI-generated video and TTS, with word budgets per duration, a spoken-style pass, a normalization pass, conservative emotion tagging from per-model dictionaries (ElevenLabs, Gemini, OpenAI, Fish Audio, Hume, Chatterbox, or a new one researched on demand), and duration validation. Use when writing, editing, reviewing, or timing narration, voiceover, V.O., or TTS input for videos, explainers, shorts, ads, or product tours — and when the user asks for a script to be read aloud, generated as speech, or fitted to a scene duration.
---

# Voiceover Scriptwriting

Write narration that sounds like someone talking, not an article being read. Every rule exists because spoken audio fails differently from prose: no re-reading, no scanning back, one chance per second.

The minimum deliverable is always a **polished script that fits the spec** (duration, channel, audience, message). Tagging, audio generation, and duration validation layer on top when the TTS model and scene durations are known.

All paths in this skill are relative to the skill's own folder — resolve `references/` and `scripts/` from wherever the skill is installed. The scripts are dependency-free Python 3.

## Step 0 — Intake: ask before drafting

Collect the variables. **Ask for anything missing** — do not guess load-bearing values. Ask once, in a single message, in the user's language.

| Variable | Required | If missing |
|---|---|---|
| Purpose & channel | Yes | Ask. (Explainer? Short? Ad? See `references/channels.md` for the list.) |
| Duration (total, or per scene) | Yes | Ask. Suggest a default per purpose if the user has no preference. |
| Core message + CTA | Yes | Ask. One message, one CTA — see the three-point rule. |
| Audience | Preferred | Infer from the brand file if one exists; otherwise ask or state your assumption. |
| TTS model / provider | For tagging | Ask which model will voice it. If it isn't covered by a `references/tags-*.md` dictionary, search the vendor's current documentation and write a new `references/tags-{provider}.md` following an existing dictionary's structure — then use it. |
| Brand file | Preferred | If none exists, ask whether the brand has an existing guide to distil (below). Failing that, offer onboarding. If declined, use the conservative default voice and flag the gap. |
| Voice (clone ID / prebuilt voice) | For generation | Only needed when actually generating audio. |
| Language & locale | Default English | Ask if the audience or brand implies otherwise. |
| Compliance | Situational | EU audience → disclosure required. Cloned voice → confirm consent exists (see Compliance). |

**Bring your own guidelines (preferred over interviewing):** if the brand already has a messaging guide, style guide, or voice-and-tone doc, ask for it first and distil it into `references/brands/{brand}.md` using `references/brand-file-template.md`. Read the source in full, map it onto the template, copy approved claim wording verbatim, record provenance (source, location, date distilled) in the header, and mark anything the source does not cover as an explicit gap. Then ask only about the gaps. A written guide rarely covers the spoken-word fields — pacing, pronunciation, voice identity, consent, emotional guardrails — so expect those to be the questions you still need to ask.

Do not work from the long guide directly each turn: long documents get partially read, and nobody can tell which half was applied. The brand file is a short, refreshable cache of it, not a replacement. When the source changes, re-distil and update the date.

**Onboarding (no brand file and nothing to ingest):** offer a 6-question interview and write the answers to `references/brands/{brand}.md` using `references/brand-file-template.md`:
1. Who is the audience, specifically?
2. Three to five voice adjectives a designer would defend in review?
3. What does this brand *never* sound like (anti-examples)?
4. Words and phrases the brand uses / avoids? Any names with tricky pronunciation?
5. Two lines of real brand copy, read aloud — one that sounds right, one that doesn't?
6. Is the voice cloned or prebuilt? Whose voice, and is consent documented?

If the user can't answer everything, fill gaps with the most conservative choice consistent with what you learned — never your trained default — and record assumptions in the brand file so they can be corrected.

**Load on demand:** the shape of a finished deliverable → `references/example-script.md`; channel details → `references/channels.md`; tag syntax for the chosen model → `references/tags-{model}.md`; brand material → the brand file; voice-clone, mixing, and pipeline techniques → `references/advanced-techniques.md`.

## Word budgets

Natural spoken English is 130–150 words per minute. Calibrate: 120 WPM = slow, dramatic; 150 = natural conversational; 180 = fast, energetic. Short-form tightens to 120–140 WPM.

Plan to **~150 WPM and aim at the low end of each range** — pauses and breaths eat roughly 8% of nominal capacity, so the top of a range is only safe for simple words and short clauses. Or run `scripts/check_duration.py`, which does the math:

| Duration | Plan for (words) | Slow 120 (words) | Fast 180 (words) |
|---|---|---|---|
| 15s | 30–40 | 25–30 | 40–45 |
| 20s | 40–50 | 35–40 | 50–55 |
| 30s | 70–80 | 55–65 | 80–90 |
| 60s | 140–150 | 110–120 | 160–180 |
| 90s | 210–225 | 165–180 | 240–270 |
| 2min | 280–300 | 220–240 | 320–360 |

Two different allowances, easy to confuse: the ~8% above is breathing room *inside* the read, while the 10–15% scene buffer under **Duration check** is headroom *around* it, because TTS output length is never exactly predictable. A scene-based script needs both.

Pauses, difficult terms, and brand names reduce real capacity further. **If the script runs long, cut a point — never speed up the read.** Rushed delivery hurts comprehension and makes the video feel cheap. Fast delivery is only safe over simple words and short clauses; slow down around brand names, numbers, instructions, and disclaimers.

Purpose defaults when the user has no duration preference: homepage hero 60–90s; organic social 15–60s; product page 90s–2min; paid ad 15–30s; sales enablement 2–3min; internal training 3–5min.

## Write for the ear

- **One idea per sentence.** Active verbs, concrete nouns, everyday words. Long nested sentences force too much information between breaths.
- **Short lines.** Under ~8 words where possible. Vary sentence length — no three consecutive sentences of the same length.
- **Conversational tone.** First person, contractions, personalization: "you" and "your", not "users". Write real spoken text — "Oh uh yeah, I think..." is legal if it's true to the brand.
- **Say it out loud as you write.** If you stumble, rewrite.
- **No prose tells.** No negative parallelism ("not just X, it's Y"), no marketing puffery ("unlock", "supercharge", "seamless", "effortless"), no significance inflation, no rule-of-three filler. Speak like a person, not an announcement.
- **Readability:** plain adult language, roughly 8th-grade level — but never childish.

**Punctuation is your rhythm notation.** Commas give breath, periods cut, ellipses and em dashes create a beat, ALL-CAPS marks emphasis. Punctuation shapes delivery but adds no fixed silence — intentional pauses belong in the performance layer (tags or a `[pause]`-style notation) and must be counted in the timing.

**Three-point rule:** one problem, one solution, one proof point. An explainer that tries to say everything says nothing memorably.

**Hook:** the first 1–3 seconds decide watch-or-scroll. State the problem or payoff immediately; never open with a logo, company introduction, or slow pan. Micro-structure: second 1 = pattern interrupt, second 2 = clear benefit, second 3 = proof or preview. If a hook underperforms, rewrite the hook — don't reshoot.

**CTA:** protect it by shortening the setup, not rushing the final words. For loopable Shorts, put the CTA in the caption — a spoken "follow for more" breaks the loop.

## Normalization pass (mandatory)

Numbers, dates, symbols, and acronyms are where TTS reads fail — "11" is "Eleven" in English, "Once" in Spanish, "Elf" in German. **Write everything exactly as it should be spoken**, in the script text:

- Numerals → words: "11" → "eleven"; "2026" → "twenty twenty-six".
- Symbols → words: "$4" → "four dollars"; "%" → "percent"; "&" → "and".
- Abbreviations → spoken form: "etc." → "and so on"; "Dr." → "Doctor" (or the spoken title).
- URLs and email addresses → spoken form or cut; they rarely survive a read.
- Unfamiliar acronyms → spell out, or use phonetic spelling if pronunciation is non-obvious.

Run `scripts/lint_normalization.py` on the draft and fix every finding. Normalizing in the text is cheaper and more reliable than runtime normalization (which also adds API latency).

## Tag pass (only when the TTS model is known)

Tags are **model-specific** — a skill that hard-codes one syntax breaks on the next. Load the dictionary for the chosen model before tagging. Six ship with the skill: ElevenLabs (`tags-elevenlabs.md`), Gemini (`tags-gemini.md`), OpenAI (`tags-openai.md`), Fish Audio (`tags-fish.md`), Hume (`tags-hume.md`), and Chatterbox (`tags-chatterbox.md`, FOSS). **Any other provider:** search the vendor's current docs and write a new `references/tags-{provider}.md` in the same shape before tagging — the structure is the standard, not any one file. If no docs can be found, deliver a model-neutral script and say tagging is pending.

Tag **peaks and valleys, not every line** — over-tagging produces audio that shifts register sentence by sentence. A proven pattern is to do the tag pass as a separate editorial step, like a voice director marking a script.

## Duration check

Run `scripts/check_duration.py` on the final script. It estimates spoken length from word count and WPM, strips tags from the count, and compares against the target. If you cannot execute files (e.g. a web assistant with no filesystem), estimate from the word-budget table instead and say that the script check was skipped — never claim a check ran that didn't.

- Over budget → cut a point, tighten the setup (protect the CTA), shorten sentences. Never "read faster".
- Scene-based work: build a 10–15% buffer into each scene's duration — TTS does not guarantee narration fits the scene. Pass `--json script.json` to validate per scene.
- A 15-second placement should not require exactly 15.00 seconds of uninterrupted speech.

## Output format

Deliver the polished script in this shape (adapt to the user's tooling):

```
## Voiceover script — {title}

**Duration:** 60s target · 148 words @ ~150 WPM · **Channel:** Explainer
**TTS:** ElevenLabs v4 · Voice: {name or voice ID} · **Brand:** {name}

---

### Scene 1 — Hook (0:00–0:05)

[excited] Stop scrolling — your monthly report just wrote itself.

*Visual: dashboard assembling itself; caption on screen.*

### Scene 2 — Problem (0:05–0:25)

...
```

Rules for the deliverable:
- Narration lines are exactly what the TTS should speak — normalized, tagged, punctuation-as-direction included.
- Scene headers carry time ranges; visual notes are clearly separated (italic / separate field) so they never get read aloud.
- If the pipeline consumes `script.json`, also emit one TTS-ready narration string per scene with `scene_id`, `duration` (target + 10–15% buffer), `narration`, and `visual_description`.
- Offer a clean read-through copy (tags stripped) for human review.

## End-to-end generation (when asked to produce audio)

One TTS call per scene; regenerate only the changed scene on edits. Keep the request contract per model (style fields, tags, verbatim transcript). Mix music under narration at ~20% volume; avoid lyric-heavy music under 180-WPM narration. Targets: peaks −12 to −6 dB, loudness ~−16 LUFS for podcast-style output. See `references/advanced-techniques.md` for the full pipeline, mixing commands, and voice-changer technique.

## Compliance (never skip)

- **Cloned voices need documented consent** from the person whose voice is used; note the clone's provenance in the brand file.
- **Synthetic audio reaching EU audiences must be disclosed** (EU AI Act Article 50); non-disclosure risks fines up to €15M or 3% of worldwide turnover.
- Conversational AI characters must tell users they're artificial unless obvious from context.
- Never express anger, sarcasm, or inappropriate excitement on a brand's behalf, whatever the script pushes toward — guardrails live in the brand file.

## Self-check before presenting

1. Fits the duration budget (script-verified, buffer included)?
2. One message, three points max, hook in the first 3 seconds, CTA protected?
3. Spoken-style pass done — one idea per sentence, short lines, no prose tells?
4. Normalization lint clean — zero numerals, symbols, or raw abbreviations in narration?
5. Tags (if any) valid for the target model, on peaks only?
6. Would a listener believe a human wrote it?
