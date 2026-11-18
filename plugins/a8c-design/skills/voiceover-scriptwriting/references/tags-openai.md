# Tag dictionary — OpenAI (gpt-realtime / TTS audio models)

OpenAI voice models use **no tag syntax at all**. Delivery is steered through prompt structure and natural language. Anything tag-like left in the transcript risks being read aloud as text.

## How direction works

1. **Prompt sections.** Structure the steering prompt with labeled sections — the model finds and follows them:

```
# Role & Objective         — who the speaker is; what success means
# Personality & Tone       — voice and style to maintain
# Context                  — the script and any retrieved info
# Reference Pronunciations — phonetic guides for tricky words
# Instructions / Rules     — do's and don'ts
# Conversation Flow        — states and transitions (interactive use)
# Safety & Escalation      — fallback and handoff (interactive use)
```

2. **Persona in the Role section.** Identity and accent are pinned in plain language — and followed tightly:
   > "You are a french quebecois speaking customer service bot. Your task is to answer the user's question."

3. **Example phrases.** The model strongly follows sample phrases — supply one or two lines read *exactly* the way the brand should sound.

4. **Style in natural language.** Describe delivery directly: "Speak warmly, at a relaxed conversational pace. Sound like a knowledgeable friend, not an announcer."

## Mandatory suppression line

Include this instruction when you want clean narration:

> "Do not include any sound effects or onomatopoeic expressions."

Without it, models may insert audible artifacts (stings, boings, "whoosh" noises) where the text implies action.

## Supporting techniques

- **Capitalized emphasis in rules** makes instructions easier to follow ("NEVER mention pricing").
- **Pin the output language** explicitly to prevent unwanted switching mid-piece.
- **Precise wording matters**: small wording changes can flip behavior — iterate.
- **Phonetic respelling** for difficult names goes under Reference Pronunciations ("Nguyen ≈ 'n-WIN'"), in the prompt — not in the transcript.
- A "variety rule" ("Vary phrasing; do not repeat sentence openings") reduces robotic delivery in longer pieces.

## What not to do

- No bracket tags, no SSML, no angle brackets in the transcript.
- Don't put direction inside the narration text — put it in the prompt sections.
- Don't rely on the transcript for sustained tone; a single style sentence in Personality & Tone carries the whole read.
