#!/usr/bin/env python3
"""check_duration.py — estimate spoken length of a voiceover script and compare it to the target.

Usage:
    python3 check_duration.py script.md --target 60
    python3 check_duration.py script.md --wpm 130 --target 30 --buffer 0.15
    cat draft.txt | python3 check_duration.py - --target 60
    python3 check_duration.py --json script.json --wpm 150

Plain-text mode counts narration words only: it strips [tag] and <tag> performance
notation, markdown headers, bold metadata lines, italic visual-note lines, bullets,
and table rows. JSON mode expects a list of scenes (or an object with a "scenes"
list), each with "narration" (str) and "duration" (seconds, already including the
scene's buffer); every scene is validated individually.

Exit code 0 if within budget, 1 if over (or on input errors), so it can gate CI.

Defaults: 150 WPM (natural conversational). Calibration points: 120 WPM = slow,
dramatic; 180 WPM = fast, energetic. The default buffer is 12% (use 10-15%): TTS
does not guarantee narration fits the scene, so narration must fit within
target * (1 - buffer).
"""

import argparse
import json
import re
import sys

WPM_DEFAULT = 150
BUFFER_DEFAULT = 0.12

# Performance notation and non-narration lines to exclude from the word count.
TAG_RE = re.compile(r"\[[^\]]*\]|<[^>]*>")
ITALIC_LINE_RE = re.compile(r"^\*[^*].*\*\s*:?\s*$")
NON_NARRATION_PREFIXES = ("#", "**", "*", ">", "---")
WORD_RE = re.compile(r"[A-Za-z0-9'’]+(?:[-'’][A-Za-z0-9'’]+)*")


def count_words(text: str) -> int:
    """Count speakable words: performance tags, markup, and non-narration lines excluded."""
    text = TAG_RE.sub(" ", text)
    kept = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(stripped.startswith(p) for p in NON_NARRATION_PREFIXES):
            continue
        if ITALIC_LINE_RE.match(stripped):
            continue
        kept.append(stripped)
    return sum(len(WORD_RE.findall(line)) for line in kept)


def estimate_seconds(words: int, wpm: float) -> float:
    if wpm <= 0:
        raise ValueError("WPM must be positive")
    return words / wpm * 60.0


def report_plain(words: int, wpm: float, buffer_frac: float,
                 target: float | None) -> int:
    est = estimate_seconds(words, wpm)
    slow = estimate_seconds(words, 120)
    fast = estimate_seconds(words, 180)
    print(f"Narration words: {words}")
    print(f"Estimated read:  {est:.1f}s at {wpm:.0f} WPM "
          f"(range {slow:.0f}s at 120 WPM — {fast:.0f}s at 180 WPM)")
    if target is None:
        print("No target given — estimates only.")
        return 0
    max_seconds = target * (1.0 - buffer_frac)
    max_words = int(max_seconds / 60.0 * wpm)
    print(f"Target: {target:.1f}s, buffer {buffer_frac:.0%} -> "
          f"narration must fit {max_seconds:.1f}s (~{max_words} words)")
    if est <= max_seconds:
        slack = max_seconds - est
        print(f"PASS — {slack:.1f}s of slack ({words_to_cut(words, max_words)} words of headroom).")
        return 0
    over_words = words - max_words
    over_seconds = est - max_seconds
    print(f"OVER by ~{over_seconds:.1f}s (~{over_words} words). "
          "Cut a point or tighten the setup — never speed up the read. Protect the CTA.")
    return 1


def words_to_cut(words: int, max_words: int) -> str:
    headroom = max_words - words
    return str(headroom) if headroom >= 0 else f"-{abs(headroom)}"


def report_json(path: str, wpm: float, buffer_frac: float) -> int:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        return 1
    scenes = data.get("scenes", data) if isinstance(data, dict) else data
    if not isinstance(scenes, list) or not scenes:
        print("error: expected a JSON list of scenes (or an object with a 'scenes' list)",
              file=sys.stderr)
        return 1

    failures = 0
    print(f"{'scene':>8}  {'words':>6}  {'est':>6}  {'scene':>6}  {'max':>6}  verdict")
    for i, scene in enumerate(scenes, start=1):
        try:
            narration = scene["narration"]
            duration = float(scene["duration"])
        except (KeyError, TypeError, ValueError) as exc:
            print(f"error: scene {i} missing 'narration' or valid 'duration': {exc}",
                  file=sys.stderr)
            return 1
        sid = scene.get("scene_id", i)
        words = count_words(narration)
        est = estimate_seconds(words, wpm)
        # Duration fields are expected to already include the scene's buffer;
        # validate against the buffer-adjusted ceiling either way.
        max_seconds = duration * (1.0 - buffer_frac)
        ok = est <= max_seconds
        verdict = "PASS" if ok else f"OVER by ~{est - max_seconds:.1f}s — cut ~{words - int(max_seconds / 60.0 * wpm)} words"
        print(f"{str(sid):>8}  {words:>6}  {est:>5.1f}s  {duration:>5.1f}s  {max_seconds:>5.1f}s  {verdict}")
        if not ok:
            failures += 1
    total_est = sum(estimate_seconds(count_words(s["narration"]), wpm) for s in scenes)
    total_dur = sum(float(s["duration"]) for s in scenes)
    print(f"\nTotal: est {total_est:.1f}s of narration across {total_dur:.1f}s of scene time.")
    if failures:
        print(f"{failures} scene(s) over budget. Cut a point per scene — never speed up the read.")
        return 1
    print("All scenes within budget.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Estimate spoken length of a voiceover script and check it against a target.",
        epilog="Word counts exclude [tags], <tags>, headers, metadata, and visual notes.",
    )
    parser.add_argument("file", nargs="?", help="script file (plain text/markdown), or '-' for stdin")
    parser.add_argument("--json", metavar="SCRIPT_JSON",
                        help="validate a script.json of scenes ({scene_id, duration, narration})")
    parser.add_argument("--target", type=float, metavar="SECONDS",
                        help="target duration in seconds")
    parser.add_argument("--wpm", type=float, default=WPM_DEFAULT,
                        help=f"speaking rate (default {WPM_DEFAULT}; 120 slow / 150 natural / 180 fast)")
    parser.add_argument("--buffer", type=float, default=BUFFER_DEFAULT,
                        help=f"headroom fraction (default {BUFFER_DEFAULT}; use 0.10-0.15)")
    args = parser.parse_args()

    if args.json:
        return report_json(args.json, args.wpm, args.buffer)

    if not args.file:
        parser.error("give a script file, '-' for stdin, or --json SCRIPT_JSON")
    try:
        if args.file == "-":
            text = sys.stdin.read()
        else:
            with open(args.file, encoding="utf-8") as f:
                text = f.read()
    except OSError as exc:
        print(f"error: cannot read {args.file}: {exc}", file=sys.stderr)
        return 1

    words = count_words(text)
    if words == 0:
        print("warning: no narration words found — check the input format", file=sys.stderr)
    return report_plain(words, args.wpm, args.buffer, args.target)


if __name__ == "__main__":
    sys.exit(main())
