# Spoken-word brand file — template

Complete once per brand, or have the agent complete it via the onboarding interview (SKILL.md, Step 0). Save as `references/brands/{brand}.md`. Delete this instruction block when saving.

Two rules make this work: **examples, not adjectives** (real lines teach voice; "warm and friendly" teaches nothing) and **negative constraints** (anything not forbidden defaults to the model's average). A stale file calcifies last year's voice — refresh it with new best-of reads as the brand evolves.

---

# {Brand name} — spoken-word brand file

## 0. Source and provenance

Fill this in whenever the file was distilled from an existing guide, so a reader can get back to the original.

- **Distilled from:** (title and where it lives)
- **Date distilled:**
- **Supersedes:** (any older doc this replaces)
- **Deliberately not captured:** (whatever lives in the source but has no slot here)
- **Still unanswered by the source:** (written guides rarely cover pacing, pronunciation, voice identity, or consent — list what still needs a human)
- **Refresh by:** re-distilling from the source, not hand-patching this file

## 1. Snapshot

- **Audience:** (be specific — "mid-level marketing managers at enterprise SaaS", not "marketers")
- **Segments:** (if the brand serves distinct audiences, name them and what shifts between them — a developer and a first-time creator do not get the same read)
- **Language(s) & locale(s):**
- **Primary channels:** (explainer / Shorts / ads / product tours)
- **Default pacing:** (WPM target and slow-fast calibration for this brand)

## 2. Voice personality → style strings

3–5 traits a designer would defend in review, each translated to a TTS style string. Weak: "professional, friendly, modern". Strong: "dry, plain-spoken, warm, precise".

| Trait | Intensity (1–5) | Style string(s) for TTS |
|---|---|---|
| (e.g. warm) | 4 | "warm and enthusiastic" |
| (e.g. plain-spoken) | 5 | "conversational, unhurried" |

## 3. Archetype → voice persona

Which voice carries the brand, and why (the archetype in one line). Immutable traits (age, gender, permanent accent) live here, not in per-request style.

- **Voice:** prebuilt voice name, or clone with `voice_...` ID
- **Clone provenance:** whose voice, source recordings, when cloned, which model
- **Consent:** documented? where? (required for cloned voices)
- **Disclosure:** does this brand's output need AI-audio disclosure? (required for EU audiences)

## 4. Words we use / words we avoid

Preferred vocabulary is also a pronunciation decision.

- **Use:** (e.g. "teams" not "users"; product names in full)
- **Avoid:** (banlist — marketing puffery plus brand-specific bans)
- **Pronunciation:** names and terms with phonetic spellings or IPA (e.g. "Automattic → o-toe-MAT-tic")

## 5. Read-aloud pairs (calibration)

Two or three before/after lines — same sentence, wrong read vs. right read, with a note on what changed. These are what the agent calibrates against.

- ❌ "Hello everyone, and welcome to yet another exciting product update!" → ✅ "Here's what shipped this week." *(no announcer energy; lead with the news)*

## 6. Emotional guardrails

- Never express: (typically: anger, sarcasm, inappropriate excitement — whatever the brand forbids)
- Emotional range allowed: (which peaks are on-brand?)
- Situations requiring extra care: (bad news, outages, pricing)

## 7. Claims: what may and may not be said

Spoken claims are harder to caveat than written ones — there is no asterisk in audio. Copy approved wording **verbatim**; never let a read round a figure up or turn a track record into a guarantee.

| Approved claim (exact wording) | Forbidden version | Why |
|---|---|---|
| | | |

- **Numbers that may be spoken:** (with their source, and their normalized spoken form)
- **Capabilities that must not be claimed:**

## 8. Hard constraints

- Reading level: (default: plain adult, ~8th grade)
- Sentence length cap: (default: under ~8 words where possible)
- Contractions: (default: yes, always)
- Exclamation marks: (default: none)
- Numbers/dates: (style decisions — "twenty twenty-six" vs "two thousand twenty-six")

## 9. Sonic identity

- Music: (genres, energy, what's banned; music mixed ~20% under narration; no lyric-heavy beds under fast narration)
- Sonic logo: (if one exists — note: a sonic logo at the end **breaks a looping Short**; place it only in non-loop formats)
- Sound palette: (SFX allowed / banned)

## Maintenance

Refresh with new best-of reads as the brand evolves. Cadence: (monthly / quarterly / per release). Owner: (who).
