---
name: feedback-triage
description: Turn a large batch of feedback (a call transcript, Granola notes, a Slack thread, a review doc, Linear comments, a blog post) into a triage page the user decides on item by item (Do it, Park, Skip, plus notes), then build the approved items one branch at a time and attach each result back to its item. Use this whenever someone wants to "go through the action items", "triage this feedback", "summarize what came out of the call and let me decide", "turn this transcript into tasks", or hands over a long meeting or review with many moving pieces, even if they don't name a page or a workflow. Also use it to resume a triage started earlier ("read my decisions", "I've marked everything, go").
compatibility: "Best in Claude Code signed in to claude.ai, where the page is an Artifact with a shared store. Elsewhere the page runs as a local HTML file and the user hands decisions back with its export button. Recommended: connectors for wherever the feedback lives (Granola, Slack, Linear, GitHub), gh CLI. Optional: a browser tool for checking builds."
---

# Feedback triage

A long call or review produces dozens of points: commitments, asks, half-ideas, strategy, personal follow-ups. Planning is most of the work. The rest goes fast once every point is written down, decided, and scoped. This skill runs that loop end to end:

1. Get the whole source.
2. Extract every item, precisely.
3. Publish a triage page the user decides on.
4. Read the decisions back and confirm them.
5. Plan the work: one branch per concern.
6. Build each batch and attach the result to its item.
7. Report.

The page is the shared record throughout. The user decides there, Claude reports progress there, and it doubles as the follow-up list for whoever gave the feedback. It suits teams with a regular feedback rhythm (a weekly sync, a design review, a stakeholder call): every call becomes one page, and the page stays useful until the last PR merges.

If your feedback is scattered across Slack, Linear and Figma, gather it into one doc first. This skill picks up from there: deciding on each point, building it, and closing the loop.

## 1. Get the whole source

Precision depends on reading all of it, so this step matters more than it looks.

- **Granola.** `get_meeting_transcript` returns only about the first 80k characters and reports `truncated` with a `next_offset`, which the tool often can't accept. After one failed attempt, ask the user for an export straight away rather than hunting for workarounds (caches, subagents, scraping, partial queries). Granola exports to a `.md` file. In it, `Me:` is the user and `Them:` is the other person on the call. `get_meetings` gives a useful AI summary, but it is a summary: it misattributes speakers and drops details.
- **Other sources.** Slack threads, Linear issues, blog posts and GitHub PRs come through whatever connectors the session has (an MCP server, `gh`). Pasted notes and local files can be read directly. If a source can't be reached, ask the user to paste or export it.
- **Read everything.** For long files, read in line ranges until you have covered the whole thing. Note who said what, and keep the source's own words for quoting.
- **Names.** Transcripts mangle proper nouns (people, products, tools). Check names against the notes, calendar title or ticket before using them.

## 2. Extract the items

Be exhaustive first, then organize. Include commitments ("I'll work on it tomorrow"), requests, design feedback, ideas floated, open questions nobody answered, strategic context, and small personal follow-ups. Include items that clearly aren't actionable now, and mark their horizon instead of dropping them: the user wants to skip those deliberately, not lose them.

Group items into **areas** by surface or topic, ordered so the areas the user can act on now come first. Give each item a short, stable id per area (`G1`, `E2`, …). Each item has:

- **Title.** The action, in plain words.
- **Summary.** What was said and why it matters, with names attached ("Priya wants…", "Sam noted…").
- **What to do.** Concrete steps, specific enough to build from.
- **Quotes.** One to three verbatim lines from the source, each with its speaker. Copy them from the transcript, not from a summary. Trim filler at the ends only.
- **Horizon, size, owner.** Owner is whoever actually committed. Someone raising an issue doesn't make it theirs.
- **Recommendation.** Do it, Park or Skip, with one honest sentence of reasoning: committed on the call, cheap, blocked, belongs to another team, and so on.

Never invent links. If an item references a ticket, look it up through the tracker's connector and use the real URL, or leave the link out. Follow the user's writing preferences (CLAUDE.md, memory) and default to US English and plain words.

## 3. Publish the triage page

1. Write the data as JSON following `references/data-and-store.md`. `assets/example-data.json` is a complete example. Set `author` to the user so the page credits who ran the triage.
2. Render it: `python3 scripts/render.py data.json triage.html`. The script validates ids, areas, decisions and quotes before writing.
3. Put the page where the user can work on it. The page is already designed to the Automattic brand, so it needs no further design pass.
   - **With the Artifact tool** (Claude Code signed in to claude.ai): call it with `action: "quickstart"` and `intent: "other"` (the tool requires this before a new artifact). Then publish `triage.html` with `capabilities: {"db": {}}`, the `icon` `grid`, and a one-sentence description. Check the store answers: `ArtifactData` `list` on `decisions` should return empty.
   - **Without it:** save `triage.html` somewhere durable (beside the source, or in the repo's ignored working notes) and give the user its path to open in a browser. The page works the same, keeps choices in that browser, and shows **Copy decisions** and **Download** buttons for handing them back.
4. Give the user the link or path with a short orientation: what's on the page, the two or three areas that matter most, and anything time-sensitive. Without the Artifact tool, tell them to press **Copy decisions** and paste the result into the chat when they're done.

**Sharing the page.** As an Artifact, it's private until the user shares it from the page's Share menu, with people in the organization or invited guests. What each access level can do:

- **Viewer or Commenter:** sees every item, decision and progress note, but can't mark anything.
- **Contributor:** can mark items and write notes. There is one decision per item, shared by everyone, so the last person to click wins.
- **Editor:** can also republish the page, so an Editor running this skill in their own session can update it.

As a local file, the page can be sent or hosted anywhere static (it's one self-contained HTML file). Each person's choices stay in their own browser, so collect one export per person and merge them, saying where they disagree.

## 4. Read the decisions back

When the user says they're done, read everything before starting:

- With the Artifact store: `ArtifactData` `list` on `decisions` (limit 100). Without it: the JSON the user pasted, or the `-decisions.json` file they downloaded. Its `decisions` object has the same fields as the store's docs, one entry per item, with `decision: null` for anything left undecided.
- Confirm the count matches the number of items, and name any left undecided. A `GENERAL` entry holds the "Anything else" note.
- Say how many items are Do, Park and Skip.
- Restate how you read each note, one line per note. Notes often change scope ("don't remove it, move it"; "flag early if anything is lost"; "use the design system's badges, not dots"), and getting one wrong costs a branch.
- Some choices are genuinely the user's to make and can't be settled from the code, such as which codebase or route a change belongs in. Ask those with `AskUserQuestion`, with your recommendation first. Settle anything else yourself and mention it.

## 5. Plan the work

- **Batches.** Group Do items by concern: one batch per coherent change, ordered by commitments first, then by dependency.
- **Branches.** One local branch per batch, cut fresh from the main branch, so the user can test one batch at a time. Stack a branch on another only when it truly depends on it, and say so. Commit locally and don't push until the user has tested, unless they say otherwise.
- **Seed the page.** Write a `progress` doc for every Do item in one `ArtifactData` batch, with status `planned` and the branch name. Items the user owns personally (watch a recording, use a test site) get status `note` and say so. Without the store, keep the same docs in a `progress.json` beside the page and re-render with `python3 scripts/render.py data.json triage.html --progress progress.json`. The user reloads the page to see it; their choices survive, because they live in the browser.
- **Read the repo's rules.** Check its own instructions (CLAUDE.md, AGENTS.md, design guidance) before the first batch. Map the relevant code once, with an Explore agent for broad sweeps, rather than rediscovering it per batch.

## 6. Build each batch, then attach the result

For each batch:

1. **Branch** from the main branch, or from the batch it depends on.
2. **Implement.** Read the surrounding code first and match its idiom and comment density. Apply the user's notes literally.
3. **Run the tests.** Where tests encode decisions (copy, structure), update an assertion only when the intent still holds, and say so in the commit. Add a short test that records the new decision.
4. **Check it in a browser.** Load a real build and look at the actual states. Hard reload after switching branches, because cached bundles show the previous branch. If the dev server fails, serve the built output statically.
5. **Commit locally.** The message says what changed and why, in plain words, and credits where the feedback came from.
6. **Attach the result.** Update the item's `progress` doc (or its entry in `progress.json`, then re-render) with status `ready`, a summary of what changed, how to test (the branch, the URL, which toggles), links (tickets, PRs), and a `followUp` note written for the person who gave the feedback.

Not every Do item is code. A "compare and decide" item gets status `note` with the findings and a recommendation. Don't make a change the user asked to be careful about until they've seen the analysis.

Keep the user posted with a line per batch as you go, and keep the details on the page.

## 6b. Open PRs and link them

Only once the user has tested a branch and says to push it, since pushing and opening a PR are visible to others:

1. Push the branch and open the PR with `gh`, following the repo's PR conventions and the user's memory notes on PR descriptions (style, AI-use disclosure, no session URLs). If `gh` can't reach the host, check the repo's own instructions for proxy or host settings before calling it unreachable.
2. Read the PR number and URL back from `gh` rather than building them by hand.
3. Write `pr: { number, url, state }` and `status: "pr"` to the `progress` doc of every item that branch covers, in one `ArtifactData` batch (or in `progress.json`, then re-render). The chip appears on each item, and the **PRs** filter collects them.
4. When the user asks for a refresh later, check each PR's state with `gh pr view` and update `state` (and `status: "merged"`) to match.

Put the triage page link in the PR description only if the user wants reviewers to see it. The page is private until they share it.

## 7. Report

End with:

- A table of branches: items, where the change lives, how many commits, and whether each is pushed (with its PR link once it is).
- Decisions you made on their behalf.
- What isn't done yet, and why.
- Where branches will conflict with each other.
- The page link, noting that the follow-up filter collects the notes for the stakeholder.

Keep it short, because the page holds the detail.

## Resuming

If the user comes back later ("read my decisions", "I've tested G4"), find the page: the artifact URL (Artifact `list`, or ask for it), or the local `triage.html` with its `data.json` and `progress.json`. Read `decisions` (from the store, or ask for a fresh export) and `progress`, and pick up from the matching step. Update the page rather than starting a new one.
