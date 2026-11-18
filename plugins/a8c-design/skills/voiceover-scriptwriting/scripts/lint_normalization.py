#!/usr/bin/env python3
"""lint_normalization.py — flag everything in a voiceover script that TTS may misread.

Numbers, dates, symbols, and acronyms are where TTS reads go wrong: "11" is
"Eleven" in English, "Once" in Spanish, "Elf" in German. The fix is to write
them out in the script exactly as they should be spoken. This linter flags
every candidate so nothing reaches generation unnormalized.

Usage:
    python3 lint_normalization.py script.md
    cat narration.txt | python3 lint_normalization.py -

Findings are ERROR (must fix — will likely be misread) or CHECK (verify the
spoken form is intended). Exit code 1 if any ERROR findings, so it can gate CI.

Narration only: headers, bold metadata lines, italic visual notes, bullets,
table rows, and [tag]/<tag> notation are ignored, same as check_duration.py.
"""

import re
import sys

TAG_RE = re.compile(r"\[[^\]]*\]|<[^>]*>")
ITALIC_LINE_RE = re.compile(r"^\*[^*].*\*\s*:?\s*$")
NON_NARRATION_PREFIXES = ("#", "**", "*", ">", "---")

# (label, pattern, level, hint) — evaluated per line, first match wins per span,
# so the most specific rules (ordinal, time, range) come before the generic number rule.
RULES = [
    ("URL", re.compile(r"\b(?:https?://|www\.)\S+", re.IGNORECASE), "ERROR",
     "URLs rarely survive a read — speak the name, or cut it"),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"), "ERROR",
     "write it out as spoken words or cut it"),
    ("currency", re.compile(r"[$£€¥]"), "ERROR",
     "write out: '$4' -> 'four dollars'"),
    ("percent", re.compile(r"%"), "ERROR",
     "write out: '%' -> 'percent'"),
    ("ampersand/plus/equals", re.compile(r"[&+=]"), "ERROR",
     "write out: '&' -> 'and', '+' -> 'plus', '=' -> 'equals'"),
    ("ordinal", re.compile(r"\b\d+(?:st|nd|rd|th)\b", re.IGNORECASE), "ERROR",
     "write out: '1st' -> 'first'"),
    ("time", re.compile(r"\b\d{1,2}:\d{2}\b"), "ERROR",
     "write out: '3:30' -> 'three thirty'"),
    ("range", re.compile(r"\b\d+\s*[-–]\s*\d+\b"), "ERROR",
     "write out: '10-15' -> 'ten to fifteen'"),
    ("decimal/number", re.compile(r"\b\d+(?:[.,]\d+)*\b"), "ERROR",
     "write out in words exactly as it should be spoken — consider the language"),
    ("abbreviation", re.compile(
        r"\b(?:etc\.|e\.g\.|i\.e\.|vs\.|approx\.|Dr\.|Mr\.|Mrs\.|Ms\.|St\.)\b", re.IGNORECASE), "ERROR",
     "write the spoken form: 'etc.' -> 'and so on', 'Dr.' -> 'Doctor'"),
    ("acronym", re.compile(r"\b[A-Z]{2,6}\b"), "CHECK",
     "spell it out or respell phonetically if the spoken form isn't obvious "
     "(deliberate ALL-CAPS emphasis lands here too — leave it)"),
]


def narration_lines(text: str):
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if any(stripped.startswith(p) for p in NON_NARRATION_PREFIXES):
            continue
        if ITALIC_LINE_RE.match(stripped):
            continue
        yield lineno, TAG_RE.sub(" ", stripped)


def lint(text: str):
    findings = []
    for lineno, line in narration_lines(text):
        # Track consumed spans so overlapping rules (e.g. a digit inside a URL) report once.
        consumed = []
        for label, pattern, level, hint in RULES:
            for m in pattern.finditer(line):
                start, end = m.span()
                if any(s <= start < e for s, e in consumed):
                    continue
                consumed.append((start, end))
                findings.append((lineno, level, label, m.group(0), hint))
    return findings


def main() -> int:
    if len(sys.argv) > 2:
        print("usage: lint_normalization.py [FILE|-]", file=sys.stderr)
        return 1
    try:
        text = sys.stdin.read() if (len(sys.argv) < 2 or sys.argv[1] == "-") \
            else open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"error: cannot read {sys.argv[1]}: {exc}", file=sys.stderr)
        return 1

    findings = lint(text)
    if not findings:
        print("CLEAN — no numerals, symbols, or raw abbreviations in narration.")
        return 0

    errors = 0
    for lineno, level, label, match, hint in findings:
        if level == "ERROR":
            errors += 1
        print(f"line {lineno:>4}  {level:<5}  [{label}] {match!r} — {hint}")
    print(f"\n{len(findings)} finding(s), {errors} must-fix.")
    print("Write every flagged item out in words exactly as it should be spoken.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
