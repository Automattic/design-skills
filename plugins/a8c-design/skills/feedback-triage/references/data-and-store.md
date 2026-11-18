# Triage page: data file and shared store

## Data file (input to `scripts/render.py`)

```json
{
  "title": "Checkout review triage",
  "slug": "checkout-review-2026-10-20",
  "intro": "Every action item, idea and open question from the call, grouped by area.",
  "source": { "kind": "Granola transcript", "label": "Weekly design sync", "date": "2026-10-20", "people": ["Priya Shah", "Sam Ortega"] },
  "author": { "name": "Sam Ortega", "url": "https://example.wordpress.com" },
  "followUpLabel": "For Priya",
  "horizons": { "now": "Now", "later": "Later", "outside": "Outside" },
  "areas": [
    { "id": "pay", "name": "Payment step", "blurb": "One sentence on what this area covers." }
  ],
  "items": [
    {
      "id": "P1",
      "area": "pay",
      "horizon": "now",
      "size": "S",
      "owner": "Sam",
      "title": "Move the saved-card picker above the new card form",
      "summary": "What was said and why it matters, with names attached.",
      "actions": ["Concrete step", "Another step"],
      "quotes": [{ "who": "Priya", "text": "Verbatim line from the source." }],
      "recommendation": { "decision": "do", "reason": "One honest sentence." }
    }
  ]
}
```

- `title` is the page name (two to four words). `intro` is one sentence. The page adds the second, muted line about marking items.
- `slug` namespaces the browser's local fallback storage. Use something unique per triage.
- `horizons` are the filter labels; keep them to one word each. `size` is `S`, `M` or `L`.
- `followUpLabel` names the person the work gets reported back to ("For Priya", "For the reviewers").
- `author` (optional) credits whoever ran the triage in the sidebar. `url` must be `https://`.
- `recommendation.decision` is `do`, `park` or `skip`.
- `GENERAL` is reserved for the page's own "Anything else" note.

## Shared store (read and written with `ArtifactData`)

As an Artifact, the page declares `capabilities: {"db": {}}`. Two collections. Without the store, the same shapes travel as files: see [Without the shared store](#without-the-shared-store).

### `decisions` (written by the page, read by Claude)

One doc per item id, plus `GENERAL`:

```json
{ "decision": "do | park | skip | null", "comment": "free text", "title": "item title", "updatedAt": "ISO time" }
```

Read them with `action: "list"`, `collection: "decisions"`, `query: {"limit": 100}`.

### `progress` (written by Claude, shown on each item and on the board)

```json
{
  "status": "planned | progress | ready | pr | merged | blocked | note",
  "branch": "design/checkout-saved-cards-first",
  "summary": "What changed, in plain words.",
  "test": "git checkout <branch>, serve the repo root, open <route>, toggle <option>.",
  "pr": { "number": 152, "url": "https://github.example.com/org/repo/pull/152", "state": "open | draft | merged | closed" },
  "links": [{ "label": "CHK-123 (Linear)", "url": "https://linear.app/..." }],
  "followUp": "A note written for the person who gave the feedback.",
  "updated": "Oct 16"
}
```

- `planned` and `note` show a grey dot, `progress` shows the signature light blue, `ready`, `pr` and `merged` show `--ok`, and `blocked` shows `--danger`. The board puts a small dot on each item's tile to match.
- Seed every Do item at once with `action: "batch"` (up to 50 writes). Creating a doc needs no `if_version`; updating one needs the `version` you last read or wrote.
- `pr` renders as a chip beside the status, linked to the PR, and the sidebar's **PRs** filter lists every item that has one. Several items often share one PR (one branch per concern), so write the same `pr` to each of them. Keep `state` current: `open` or `draft` when opened, `merged` or `closed` when that happens, and move `status` to `pr`, then `merged`, to match.
- Only `https://` links render. Never write a link you haven't verified.

## Without the shared store

When the page isn't an Artifact with a store (a local file, or a host without Artifacts), it keeps choices in the browser's `localStorage` under `triage.<slug>.v1` and shows **Copy decisions** and **Download** in the sidebar.

### Decisions export (written by the page, read by Claude)

The user pastes this into the chat or downloads it as `<slug>-decisions.json`:

```json
{
  "triage": "checkout-review-2026-10-20",
  "title": "Checkout review triage",
  "exportedAt": "2026-10-21T09:12:00.000Z",
  "decisions": {
    "P1": { "decision": "do", "comment": "Keep the form open on mobile", "title": "Move the saved-card picker…", "updatedAt": "2026-10-21T09:05:00.000Z" },
    "P2": { "decision": null, "comment": "", "title": "…", "updatedAt": null },
    "GENERAL": { "decision": null, "comment": "Start with checkout.", "title": "General notes", "updatedAt": "…" }
  }
}
```

Every item appears, with `decision: null` when undecided. `GENERAL` appears only when the note has text. Check `triage` matches the data file's `slug` before acting on it.

### Progress file (written by Claude, rendered into the page)

`progress.json` is an object keyed by item id, each value a `progress` doc as above:

```json
{ "P1": { "status": "ready", "branch": "design/checkout-saved-cards-first", "summary": "…" } }
```

Re-render with `python3 scripts/render.py data.json triage.html --progress progress.json`. The script checks each key is an item id and each `status` is valid. The user reloads to see it, and keeps their choices.
