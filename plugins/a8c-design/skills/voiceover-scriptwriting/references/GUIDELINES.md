# Voiceover scriptwriting kit: guidelines

How to use the voiceover-scriptwriting skill to get polished, on-brand voiceover scripts from any agent, and generated audio too when you want it.

## What this kit is

Writing for the ear is a different craft from writing for the page. Audio is closer to poetry than prose: what matters is cadence, pace, and a holistic sense of how the video moves. Agents default to prose habits, and the result sounds like an article being read aloud.

This kit teaches an agent the craft: word budgets that fit real durations, sentences that breathe, numbers written the way they’re spoken, and emotion direction in the syntax of whichever TTS model you use. It works like a matryoshka, with brand-agnostic principles at the core and per-brand and per-model files that load only when needed.

What’s in the box:

```
voiceover-scriptwriting/
├── SKILL.md                          ← the agent reads this first; core rules + workflow
├── references/
│   ├── GUIDELINES.md                 ← this guide (human-facing; the agent doesn't need it)
│   ├── channels.md                   ← duration targets, hooks, structures, platform grammars
│   ├── tags-elevenlabs.md            ← [square-bracket] tag dictionary (Eleven v3/v4)
│   ├── tags-gemini.md                ← <angle brackets> + style field (Gemini 3.8 Flash TTS)
│   ├── tags-openai.md                ← no tags; prompt steering (gpt-realtime & TTS voices)
│   ├── tags-fish.md                  ← [square brackets] + Drama 3 directions (Fish Audio)
│   ├── tags-hume.md                  ← natural-language acting instructions (Octave)
│   ├── tags-chatterbox.md            ← FOSS: parameters + Turbo inline tags (Resemble AI)
│   ├── brand-file-template.md        ← fill in once per brand; the agent's calibration sheet
│   ├── example-script.md             ← a worked 30s deliverable: brief → final script → script.json
│   ├── advanced-techniques.md        ← cloning, mixing, per-scene pipelines, native-audio video
│   └── brands/                       ← your completed brand files live here
└── scripts/
    ├── check_duration.py             ← does the narration fit the slot? (text or script.json)
    └── lint_normalization.py         ← finds everything TTS would misread
```

The guaranteed minimum: even with nothing but a duration and a message, the skill delivers a polished script that fits the spec. Everything else (tags, per-scene validation, generated audio) layers on when you supply more.

## Quick start: three paths

### Path A: “I just need a script”

Give the agent the essentials, or let it ask you:

> “Write a 30-second voiceover for an organic social video announcing our new reporting feature. It’ll be voiced with ElevenLabs.”

The agent asks for anything missing: audience, CTA, brand file, and which TTS provider, since tags differ per model. If your provider isn’t covered by a shipped dictionary, the agent researches its docs and writes one. It then drafts to a word budget, does a spoken-style pass, normalizes every number, tags emotional peaks in the right syntax, and checks the duration. You get a script where narration lines are exactly what the TTS should speak, with visual notes kept separate so they never get read aloud.

### Path B: “Make it sound like our brand”

Complete the brand file once. It takes about ten minutes per brand and is reusable after that.

**If the brand already has a messaging guide, style guide, or voice-and-tone doc, hand that over first.** The agent reads it in full, distils it into the brand file, records what it came from and when, and then asks you only about what the guide didn’t cover. Written guides are rarely written for the ear, so expect the remaining questions to be the spoken-word ones: pacing, pronunciation, voice identity, consent, and emotional guardrails.

Distilling beats pointing the agent at the guide each turn: long documents get partially read, and you can’t tell which half was applied. The brand file is a short, refreshable cache that names its source — when the guide changes, re-distil rather than maintaining two documents.

With nothing to ingest:

1. The agent runs a six-question onboarding interview (see below), or you fill in `references/brand-file-template.md` yourself.
2. Save it as `voiceover-scriptwriting/references/brands/{brand}.md`.
3. From then on, just name the brand: “Write the voiceover for the spring launch Short, in the {brand} voice.”

Two rules make the file work. First, examples, not adjectives: real lines the brand has actually used teach voice, while “warm and friendly” teaches a lot less than you’d think. Second, negative constraints: there’s a good chance the model will default to anything you don’t explicitly forbid. If you can’t answer a question, the agent fills the gap with the most conservative choice consistent with what you did tell it, and records the assumption in the file so you can correct it later.

**The onboarding interview (what the agent will ask you):**

1. Who is the audience, specifically? (Not “marketers” but “mid-level marketing managers at enterprise SaaS.”)
2. Which three to five voice adjectives would a designer defend in review? (“Dry, plain-spoken, warm, precise” beats “professional, friendly, modern.”)
3. What does this brand never sound like?
4. Which words and phrases does the brand use or avoid? Any names with tricky pronunciation?
5. Can you share two lines of real brand copy read aloud, one that sounds right and one that doesn’t?
6. Is the voice cloned or prebuilt? Whose voice is it, and is consent documented?

### Path C: “Generate the audio too”

Add the model, the voice, and (for scene-based work) scene durations:

> “Voice it with Eleven v4, voice ID {…}. Scenes: 3s hook, 12s problem, 15s CTA.”

The agent validates narration against each scene with the buffer, makes one TTS call per scene, and regenerates only the scenes that change during edits. The pipeline details (mixing levels, LUFS targets, FFmpeg flags) live in `references/advanced-techniques.md`.

## The variables: what the agent needs from you

With agents, just as with people, a well-defined brief makes a big difference to the quality of the output. The skill treats these as variables and asks when they’re missing rather than guessing:

| Variable | Why it matters | Default if you say “you decide” |
|---|---|---|
| Purpose and channel | Locks duration, structure, and platform grammar | Suggests one based on your message |
| Duration | Locks the word budget | Suggests the purpose default (hero 60–90s, social 15–60s, ads 15–30s, and so on) |
| Core message and CTA | One message, three points max | Asks rather than invents |
| TTS model | Tags are model-specific | Researches the provider’s docs and writes a new tag dictionary; delivers a model-neutral script if it can’t find any |
| Brand file | Voice, lexicon, guardrails | Distils an existing guide if you have one; otherwise onboarding, or a conservative neutral voice with a flagged gap |
| Voice (ID or name) | Identity | Only needed for generation |
| Language and locale | Pronunciation, normalization | English, flagged as an assumption |

The first four matter most. Duration and message alone always get you a script; the model choice unlocks tagging, and the brand file unlocks voice.

## The craft, in plain language

You don’t need to memorize any of this, since the skill applies it, but knowing why helps you brief and review.

**Word budgets.** Natural spoken English runs 130–150 words per minute, so a 60-second explainer holds about 140–150 words. At 120 WPM a read sounds slow and dramatic; at 180 it sounds fast and energetic. When a script runs long, the fix is to cut a point, not speed up the read: rushed delivery makes a video feel cheap. `scripts/check_duration.py` does this math for you, including the buffer TTS needs — 12% by default, adjustable with `--buffer`.

**Writing for the ear.** One idea per sentence, active verbs, short lines (under about eight words where possible), contractions, “you” and “your.” Punctuation is rhythm notation: commas give breath, periods cut, ellipses and dashes create a beat, ALL-CAPS marks emphasis. In a typical video you’ll want three key points at most: one problem, one solution, one proof. The hook does its work in the first three seconds, so don’t waste that moment opening on a logo.

**Normalization is where reads quietly fail.** “11” is “eleven” in English, “once” in Spanish, “elf” in German. Every number, date, symbol, and abbreviation must be written out in the script exactly as it should be spoken. The linter flags anything that slipped through; fix it in the text, not in API settings.

**Tags are conservative.** Emotion tags go on peaks and valleys, not on every line. Over-tagging produces audio that shifts register sentence by sentence, which can start to sound uncanny. Tags also aren’t portable between models (see the cheat sheet below).

**Loops (Shorts).** For loopable Shorts of 20–25 seconds, the ending echoes the opening, audio continues across the loop point, and the spoken CTA moves to the caption. A three-second “follow for more” eats up to 15% of the video and breaks the loop.

## Emotion tags: cheat sheet per model

Each platform has its own way of tagging emotion for the narrator, and those conventions can change quickly. That’s why the dictionaries live in separate files the agent loads per job. In summary:

- **ElevenLabs (v3/v4):** square-bracket tags inline, such as `[laughs]`, `[whispers]`, `[excited]`, `[pause]`; punctuation does the rest, and there’s no SSML. Trap: tags get read aloud if the voice doesn’t suit the delivery.
- **Gemini 3.8 Flash TTS:** the text is treated as a verbatim transcript. Momentary vocalizations go inline in angle brackets (`<sigh>`, `<short pause>`); sustained style goes in the `speech_metadata.style` field. Trap: direction left in the text gets spoken, and long persona paragraphs cause voice drift.
- **OpenAI (gpt-realtime and TTS voices):** no tags at all. Steer via labeled prompt sections and example phrases, and suppress artifacts with “Do not include any sound effects or onomatopoeic expressions.”
- **Fish Audio (S2 and Drama 3):** square brackets accepting a fixed tag set as well as free-form natural language (`[slightly sad]`, `[very excited]`), with `[break]` and `[long-break]` for pauses. Drama 3 adds voice-actor-style directions plus word-level paired tags like `<whisper>…</whisper>`. Trap: a missing or misspelled model header silently falls back to `s2.1-pro`.
- **Hume (Octave):** natural-language acting instructions in the utterance `description` field (keep them under about 100 characters); rate via the `speed` parameter; `[pause]` and `[long pause]` inline in the text.
- **Chatterbox (FOSS, MIT):** mostly parametric (`exaggeration`, `cfg_weight`); Turbo-class models add inline paralinguistic tags (`[laugh]`, `[chuckle]`, `[cough]`).

**Any other provider:** tell the agent which one you’re using. It will search the vendor’s current documentation and write itself a new `tags-{provider}.md` dictionary in the same shape before tagging. That’s the whole extension story: the structure is the standard, not any one file.

Full dictionaries with examples: `references/tags-elevenlabs.md`, `tags-gemini.md`, `tags-openai.md`, `tags-fish.md`, `tags-hume.md`, `tags-chatterbox.md`.

## What a finished script looks like

`references/example-script.md` holds a complete worked deliverable: the brief as given, the final 30-second script with scene headers and visual notes, the matching `script.json`, and a note on what each pass changed. It is the fastest way to see what to expect back — and a useful thing to point the agent at when you want output in a particular shape.

## Running the tools yourself

Short version: you don’t have to. When the agent works on a script, it runs these checks itself, so you’ll see them scroll past as ordinary shell commands in the agent’s transcript, like this:

```
$ python3 scripts/check_duration.py script.md --target 30
Narration words: 63
Estimated read:  25.2s at 150 WPM (range 32s at 120 WPM — 21s at 180 WPM)
Target: 30.0s, buffer 12% -> narration must fit 26.4s (~66 words)
PASS — 1.2s of slack (3 words of headroom).
```

The agent then acts on the result (cutting a point, fixing a flagged numeral) without you needing to do anything. The commands below are for when you want to check something independently, such as a script a colleague’s agent wrote, or when you’re curious.

The scripts are dependency-free Python 3, so you can run them anywhere, including CI (see “Who runs what” below).

**Does my script fit the slot?**

```
python3 scripts/check_duration.py script.md --target 30
python3 scripts/check_duration.py script.md --wpm 130 --target 60   # calmer read
```

This one makes sure your script fits the running time you gave the agent. It counts only narration (tags, headers, metadata, and visual notes are excluded), estimates the read at your WPM, and compares it against the target with the buffer applied. Exit code 1 means you’re over budget and need to cut something.

**Per-scene validation (the script.json pipeline):**

```
python3 scripts/check_duration.py --json script.json
```

Each scene needs `scene_id`, `duration` (in seconds, buffer already included), and `narration`. Every scene is checked, and the report tells you how many words to cut and repeats the rule: cut a point, never speed up the read.

**What will TTS misread?**

```
python3 scripts/lint_normalization.py script.md
```

It flags every numeral, currency or percent symbol, ordinal, time, URL, email, and raw abbreviation (exit 1 means must fix), and lists acronyms as check items. ALL-CAPS emphasis is legitimate, so acronyms are verify-not-fix.

## Who runs what (and when)

There are three layers, from most to least human.

**The agent, during the job.** This is the default. The skill instructs the agent to run the checks and act on the results itself, so you just review the script it hands back. No terminal required.

**You, for independent checks.** Copy and paste the commands above whenever you want to verify something yourself, or check work that came from somewhere else. If any of this is new to you, open a terminal, `cd` into the kit folder, and paste the command. The worst that happens is a printed report.

**CI, for enforcement without an agent.** “CI” (continuous integration) just means your repo runs checks automatically on every change, with no person or agent in the loop. The scripts are built for this: they print a report and exit with a failure code when something is over budget or must be fixed, so the repo can reject the change. Setting that up is a one-time task for whoever maintains the repo (the voiceover kit’s per-scene mode and the UX kit’s linter both work this way).

On platforms with no filesystem (pasting into a web assistant, for example), the agent can’t run the scripts, so the skill instructs it to check by hand and say so, rather than pretend a check ran.

## Troubleshooting

**Tags are being read aloud as text.** The voice doesn’t suit the requested delivery, for example a soft voice directed with `[shouts]` again and again. Try a voice with a wider emotional range, confirm the model version, or dial the tags back.

**The voice drifts or changes character mid-piece.** This is most common with Gemini, and the cause is usually long persona paragraphs or meta-instructions in the style field. Test with an empty style field first, keep style strings short and reuse them verbatim, and put immutable traits (age, accent) in voice selection, not style.

**The clone sounds flat and ignores emotion tags.** The source recordings were likely emotionally flat. Re-record with natural variety, or render the performance with an expressive model and swap identity via the Voice Changer technique (see `advanced-techniques.md`).

**The audio has artifacts, like uneven speed or odd volume.** The clone’s similarity is pushed too high. Back it off in your settings, and consider Natural mode over Creative mode for brand work.

**The script is 10% over budget and the read sounds rushed.** That’s the over-budget fix being applied wrongly. Cut a point or tighten the setup (protect the CTA); the words must fit the slot, not the other way around.

**Music fights the narration.** Mix it about 20% under the voice, and avoid lyric-heavy beds under fast narration.

## Compliance checklist (before you publish)

- [ ] Cloned voice: if it isn’t your own voice, get documented consent from the person whose voice was cloned, and note the provenance in the brand file.
- [ ] EU audience: synthetic audio needs to be disclosed wherever the video is posted (EU AI Act Article 50; non-compliance risks fines of up to €15 million or 3% of worldwide annual turnover, whichever is higher).
- [ ] Interactive or conversational audio: the AI identifies itself unless that’s obvious from context.
- [ ] The script never has the brand express anger or sarcasm, whatever the copy implies. Emotional guardrails live in the brand file.
- [ ] Default voices from big providers sound increasingly familiar. Check that the voice doesn’t undermine trust in your brand by sounding like everyone else’s.

## Maintenance

**Brand files are living documents.** Refresh them with new best-of reads as the brand evolves, since a stale file calcifies last year’s voice. Suggested cadence: quarterly, or per major release.

**Tag dictionaries are dated to October 2026.** The expressive-TTS market moves monthly, so when a vendor ships new tags or a new model, update the relevant `tags-*.md` file. The skill’s architecture is designed so that’s a one-file change.

**Test the skill itself when you change it.** Anthropic’s guidance is to run at least three evaluation scenarios across model sizes (a short-form hook, a 60-second explainer, a scene-based generation) and watch how the agent navigates the structure, rather than assuming.

## Where this came from

The design writing team’s research into AI video voiceover best practices, covering word budgets and the hook window, loop mechanics and platform grammars, the per-scene generation pipeline, and each provider’s direction syntax.

