---
name: wpds-changes
description: Summarize recent changes in the WordPress Design System — components, tokens & styles, icons, and patterns & layouts — by scanning the Gutenberg and WordPress core repositories over a timespan you choose. Produces two Markdown tables (Design System Updates + Active Discussions) plus a one-line highlight. Use when the user wants a WPDS digest or changelog, asks "what changed in the WordPress design system", "design system updates this week/month", "@wordpress/components recent changes", or types /a8c-design:wpds-changes.
argument-hint: "[24h | week | 2weeks | month]"
---

# WordPress Design System Digest

Summarizes recent activity in the WordPress Design System for a product designer. It scans the [Gutenberg repository](https://github.com/WordPress/gutenberg) and the WordPress core repository for merged pull requests, commits, and active discussions that impact the design system, then produces a concise, link-rich report.

It focuses on four areas only:

1. **Components** — UI components like Button, Modal, TextControl, etc. (`packages/components`)
2. **Tokens & styles** — Design tokens, color, typography, spacing
3. **Icons** — Changes to `@wordpress/icons`
4. **Patterns & layouts** — Block patterns, editor layouts, structural UI changes

## Step 1 — Determine the timespan

The digest analyzes a window of time ending today. Determine which window the user wants:

- If the argument already names a timespan (e.g. `24h`, `week`, `2weeks`, `month`), use it directly — skip the question.
- Otherwise, ask the user with the **AskUserQuestion** tool (header: "Timespan", question: "How far back should I analyze WordPress Design System activity?") with these four options:
  - **Last 24 hours** — changes merged in the past day
  - **Last week** — the past 7 days
  - **Last two weeks** — the past 14 days
  - **Last month** — the past 30 days

## Step 2 — Compute the cutoff date

Get today's date by running `date -u +%Y-%m-%d` with the Bash tool. Do NOT guess the date. Then subtract the chosen window to get the **cutoff date**:

- Last 24 hours → today minus 1 day
- Last week → today minus 7 days
- Last two weeks → today minus 14 days
- Last month → today minus 30 days

Use the cutoff date (formatted `YYYY-MM-DD`) in all searches below as `DATE`.

## Step 3 — Search for changes

Search GitHub (via WebSearch / WebFetch) for merged PRs and commits since the cutoff date that impact the four focus areas. Useful query shapes:

- `site:github.com/WordPress/gutenberg merged:>DATE label:design-system OR label:components`
- Recent PRs mentioning "components", "design tokens", "icons", or "patterns"
- The Gutenberg pulls view filtered by merge date and the relevant labels/packages

For each relevant change, collect:

- The name/title of the change
- A brief description of what it does
- What it used to be **before** the change
- What it is **now** after the change
- Up to 3 relevant links (PR, commit, or issue URLs) showing where the implementation happened

## Step 4 — Output the report

Produce a short report with two Markdown tables.

---

## 🔧 Design System Updates

| Change | Description | Before | After | Relevant Links |
|--------|-------------|--------|-------|----------------|

Keep this table concise — only include changes that meaningfully impact the design system. Skip bug fixes or internal tooling changes that don't affect the design system's API or visual output. Aim for 5–15 rows (fewer for the 24-hour window). If a "before" state is unclear from the PR, write "N/A". For links, use short markdown format like `[PR #1234](url)`, max 3 per row.

---

## 💬 Active Discussions

Search for open GitHub issues, PRs with active comment threads, and Gutenberg discussions from within the chosen timespan related to the WordPress design system. Include the most active or high-signal discussions.

| Discussion Title | Description | Relevant Links |
|-----------------|-------------|----------------|

Aim for 3–7 rows. Focus on discussions relevant to a product designer working on WordPress — proposed component changes, design token debates, UX pattern proposals, or accessibility conversations.

---

End with a one-sentence note on the most significant change or discussion of the period.

## Task

Run the digest for the timespan given in the arguments (asking the user if none is given): $ARGUMENTS
