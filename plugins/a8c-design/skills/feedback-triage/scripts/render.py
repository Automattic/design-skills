#!/usr/bin/env python3
"""Fill the triage template with a data file and write the page to publish.

    python3 render.py data.json out.html [--progress progress.json]

Validates the data first, so a broken page is caught here rather than after
publishing: unique item ids, every item's area exists, decisions are do/park/skip,
and every quote names who said it.

--progress embeds a map of item id to progress doc (the same shape as the shared
store's progress collection). Use it when the page has no shared store: re-render
and republish to show status, branches and PRs on each item.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "triage-template.html"
DECISIONS = {"do", "park", "skip"}
STATUSES = {"planned", "progress", "ready", "pr", "merged", "blocked", "note"}


def fail(message):
    sys.exit(f"render.py: {message}")


def validate(data):
    for key in ("title", "areas", "items"):
        if key not in data:
            fail(f"missing top-level '{key}'")
    areas = {area.get("id") for area in data["areas"]}
    if None in areas:
        fail("every area needs an 'id' and a 'name'")
    horizons = set((data.get("horizons") or {}).keys())
    seen = set()
    for item in data["items"]:
        iid = item.get("id")
        if not iid or iid in seen:
            fail(f"item id missing or repeated: {iid!r}")
        seen.add(iid)
        if iid == "GENERAL":
            fail("'GENERAL' is reserved for the page's general note")
        for key in ("area", "title", "summary"):
            if not item.get(key):
                fail(f"{iid}: missing '{key}'")
        if item["area"] not in areas:
            fail(f"{iid}: area '{item['area']}' is not in 'areas'")
        if horizons and item.get("horizon") and item["horizon"] not in horizons:
            fail(f"{iid}: horizon '{item['horizon']}' is not in 'horizons'")
        rec = item.get("recommendation")
        if rec and rec.get("decision") not in DECISIONS:
            fail(f"{iid}: recommendation.decision must be one of {sorted(DECISIONS)}")
        for quote in item.get("quotes", []):
            if not quote.get("who") or not quote.get("text"):
                fail(f"{iid}: every quote needs 'who' and 'text'")
    return seen


def validate_progress(progress, ids):
    if not isinstance(progress, dict):
        fail("progress must be an object keyed by item id")
    for iid, doc in progress.items():
        if iid not in ids:
            fail(f"progress: '{iid}' is not an item id")
        if not isinstance(doc, dict) or doc.get("status") not in STATUSES:
            fail(f"progress {iid}: status must be one of {sorted(STATUSES)}")


def main():
    args = sys.argv[1:]
    progress_path = None
    if "--progress" in args:
        at = args.index("--progress")
        if at + 1 >= len(args):
            fail("--progress needs a file")
        progress_path = args[at + 1]
        del args[at:at + 2]
    if len(args) != 2:
        fail("usage: render.py data.json out.html [--progress progress.json]")
    data = json.loads(Path(args[0]).read_text())
    ids = validate(data)
    if progress_path:
        data["progress"] = json.loads(Path(progress_path).read_text())
    if "progress" in data:
        validate_progress(data["progress"], ids)
    # Safe inside <script type="application/json">: nothing can close the tag.
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = data["title"].replace("<", "&lt;")
    page = TEMPLATE.read_text().replace("__TRIAGE_TITLE__", title).replace("__TRIAGE_DATA__", payload)
    Path(args[1]).write_text(page)
    extra = f", progress on {len(data['progress'])}" if data.get("progress") else ""
    print(f"Wrote {args[1]} with {len(ids)} items in {len(data['areas'])} areas{extra}.")


if __name__ == "__main__":
    main()
