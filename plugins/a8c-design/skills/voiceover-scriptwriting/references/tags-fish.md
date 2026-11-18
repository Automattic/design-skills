# Tag dictionary — Fish Audio (S2 family & Drama 3)

Fish Audio S2 models (S2-Pro, S2.1-Pro) and Drama 3 are directed through **square brackets**; cues accept both a fixed tag set and free-form natural language. The old S1 model used `(parentheses)` with a fixed tag set and is deprecated — parenthetical tags are not auto-converted, so rewrite them.

## Sentence-level emotion cues (place at the start of the sentence)

```
[happy] What a beautiful day!
[sad] I'm sorry to hear that.
[excited] This is amazing news!
```

**Intensity** — use modifiers or richer words: `[slightly sad]`, `[very excited]`; the intensity scale runs satisfied→happy→delighted, disappointed→sad→depressed, frustrated→angry→furious, nervous→scared→terrified, interested→excited→ecstatic.

**Basic emotions (24):** happy, sad, angry, excited, calm, nervous, confident, surprised, satisfied, delighted, scared, worried, upset, frustrated, depressed, empathetic, embarrassed, disgusted, moved, proud, relaxed, grateful, curious, sarcastic.

**Advanced emotions (25):** disdainful, unhappy, anxious, hysterical, indifferent, uncertain, doubtful, confused, disappointed, regretful, guilty, ashamed, jealous, envious, hopeful, optimistic, pessimistic, nostalgic, lonely, bored, contemptuous, sympathetic, compassionate, determined, resigned.

**Transitions:** express emotional arcs as a sequence of cues — `[happy]` → `[uncertain]` → `[sad]` → `[hopeful]` → `[determined]`.

## Tone, effects, and pauses (can appear anywhere)

- **Tone markers:** `[in a hurry tone]` `[shouting]` `[screaming]` `[whispering]` `[soft tone]` `[emphasis]` (place `[emphasis]` right before the word to stress).
- **Audio effects:** `[laughing]` `[chuckling]` `[sobbing]` `[crying loudly]` `[sighing]` `[groaning]` `[panting]` `[gasping]` `[yawning]` `[snoring]` `[clear throat]` — add the spoken text after ("Ha, ha, ha") if it helps; natural text also works without tags.
- **Special effects:** `[audience laughing]` `[background laughter]` `[crowd laughing]`.
- **Pauses:** `[break]` (short) and `[long-break]` (extended) — count these in the duration check.

## Combining

- Stack up to three cues: `[sad][whispering] I miss you so much.` — `[angry][shouting] Get out of here now!`
- Mid-sentence: `What a [warm and happy] wonderful day!`
- Free-form natural descriptions are valid: `[slightly sad]`, `[very excited]`.
- One primary emotion per sentence; space out changes; never mix conflicting emotions.

## Drama 3 extras

Drama 3 (`model: drama-3`) adds free-form **plain-language directions in brackets before the words they apply to**, briefed like a voice actor:

```
[barely holding it together, forcing a smile] I'm fine. [shaky breath] Really. [small laugh] Go on without me.
[low, gravelly, tired but in control] Sit down.
```

Directions can be in any language regardless of the script's. Word-level paired tags change delivery of only the wrapped words: `<whisper>…</whisper>`, `<emphasis>…</emphasis>`, `<soft>…</soft>`, `<fast>…</fast>`, `<slow>…</slow>`, `<stress>…</stress>`, `<forceful>…</forceful>`. Experimental language switching uses `<french>…</french>`-style tags (use a bilingual clone; test the pair).

**Trap:** a missing or misspelled `model: drama-3` header silently falls back to `s2.1-pro` — the request succeeds but the direction syntax behaves differently. Confirm the model header after config changes.

## Limits

- Markers don't count toward token limits and add no latency; 13 languages supported.
- Overuse in short text degrades delivery — tag peaks, not every line (same rule as everywhere else).
