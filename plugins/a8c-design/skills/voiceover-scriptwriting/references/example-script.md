# Worked example — 30s organic-social launch teaser

A compact end-to-end example of the expected deliverable. Brief as given: *"30-second social video announcing our reporting feature; it'll be voiced with ElevenLabs; audience is small-business owners; CTA is 'save this'."* No brand file existed, so the agent used a conservative neutral voice and flagged the gap.

## Final script

```
## Voiceover script — Reports launch teaser

**Duration:** 30s target · 55 words @ ~150 WPM · **Channel:** Organic social (TikTok/Reels)
**TTS:** ElevenLabs v4 · Voice: (neutral, wide emotional range) · **Brand:** none supplied — neutral voice used

---

### Scene 1 — Hook (0:00–0:04)

[excited] Stop scrolling — your monthly report just wrote itself.

*Visual: report assembling itself on screen; caption: "the old way →"*

### Scene 2 — Problem (0:04–0:16)

Every month, you export the numbers, rebuild the same three charts, and lose an hour to formatting. It costs you forty dollars in coffee.

*Visual: screen recording of manual chart building; clock spinning.*

### Scene 3 — Payoff + CTA (0:16–0:30)

Reports now build themselves. Save this for later — you'll want it on the first. No exports, no formatting — done before your coffee's cold.

*Visual: finished report; caption: "Save this". Loop point: audio continues into Scene 1.*
```

**What the passes did:** drafted to the timeline (hook in the first 3 seconds; the problem staged in the viewer's context; the CTA protected by keeping the payoff tight) → spoken-style pass (short clauses, active verbs, contractions) → normalization pass (wrote out "three", "forty dollars", "first" — the lint originally flagged `3`, `$40`, `1st`) → tag pass (one tag, on the peak — the hook — nothing else) → duration check (each scene fits its slot with the 12% buffer; `check_duration.py --json` verifies). Loop structure: callback hook, audio continues across the seam, CTA captioned not spoken.

## Matching script.json (for the per-scene pipeline)

```json
[
  {"scene_id": 1, "duration": 4.0, "narration": "[excited] Stop scrolling — your monthly report just wrote itself.", "visual_description": "report assembling itself; caption: the old way"},
  {"scene_id": 2, "duration": 12.0, "narration": "Every month, you export the numbers, rebuild the same three charts, and lose an hour to formatting. It costs you forty dollars in coffee.", "visual_description": "screen recording of manual chart building; clock spinning"},
  {"scene_id": 3, "duration": 14.0, "narration": "Reports now build themselves. Save this for later — you'll want it on the first. No exports, no formatting — done before your coffee's cold.", "visual_description": "finished report; caption: Save this; loop point"}
]
```

Durations include the 10–15% buffer; scene 3 leaves intentional breathing room for the music beat before the loop seam.

*Note: run `lint_normalization.py` on the narration only (a plain-text list of narration lines, or the JSON above). Linting this explanatory document flags its own prose and JSON — the narration lines themselves are clean.*
