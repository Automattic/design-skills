---
name: add-skill
description: Add a new skill to the design plugin. Use when you've built a Claude Code skill and want to contribute it to the shared Automattic design plugin — handles finding the repo, creating a branch, scaffolding files, updating metadata, and opening a PR.
argument-hint: "[path to your SKILL.md, or describe what your skill does]"
allowed-tools: Bash, Read, Write, Edit, Glob, AskUserQuestion
---

# Add Skill

Contribute a new skill to the shared `design` plugin. This workflow handles the full contribution: finding the repo, branching, scaffolding, updating all metadata, and opening a draft PR.

---

## Phase 1 — Understand the input

Look at `$ARGUMENTS`:

**If it's a file path** (contains `/` or ends in `.md`):

- Read the file
- Extract `name` and `description` from YAML frontmatter
- Show the user what was found and confirm: "Found skill `<name>` — `<description>`. Ready to contribute this?"

**If it's a description or empty**:

- Ask the user: "What should we call this skill? (kebab-case, e.g. `my-skill-name`)"
- Ask: "One sentence: what does it do?"
- Draft a minimal SKILL.md together with the user:

  ```
  ---
  name: <name>
  description: <description>
  argument-hint: "[...]"
  ---

  # <Title>

  <Body — at least a paragraph describing what the skill does and how>

  ## Task

  $ARGUMENTS
  ```

- Show the draft and ask: "Does this look right? I'll use this as the skill content."

**Validate before continuing:**

- `name` must be kebab-case (lowercase letters, numbers, hyphens only — no spaces, no underscores)
- `description` must be present and non-empty
- Body must be non-trivial (more than one line)
- Skill body must end with `$ARGUMENTS`

If any validation fails, explain the issue and ask the user to fix it before continuing.

---

## Phase 2 — Find the repo

Check these locations in order:

```bash
ls ~/Documents/GitHub/design-skills/plugins/design/.claude-plugin/plugin.json 2>/dev/null
ls ~/Source/design-skills/plugins/design/.claude-plugin/plugin.json 2>/dev/null
ls ~/code/design-skills/plugins/design/.claude-plugin/plugin.json 2>/dev/null
```

**If found:** Tell the user — "Found the repo at `<path>`. Using that." and set `REPO` to the repo root.

**If not found:** Ask the user:

> "I couldn't find the `design-skills` repo locally. Where is it? (Paste the path, or press Enter and I'll clone it)"

If they provide a path: use it as `REPO`.

If they press Enter (empty): clone the repo:

```bash
git clone REPO_PLACEHOLDER ~/Documents/GitHub/design-skills
```

Then set `REPO=~/Documents/GitHub/design-skills`.

**Before continuing:** Check that a skill with this name doesn't already exist:

```bash
ls "$REPO/plugins/design/skills/<skill-name>" 2>/dev/null
```

If it exists, tell the user and stop: "A skill named `<name>` already exists. Rename your skill and try again."

---

## Phase 3 — Create a branch

```bash
cd "$REPO"
git checkout main && git pull
git checkout -b add/<skill-name>
```

Tell the user: "Created branch `add/<skill-name>` from latest `main`."

---

## Phase 4 — Scaffold the skill

Create the directory and write the skill file:

```
$REPO/plugins/design/skills/<skill-name>/SKILL.md
```

- If the input was a file path: copy the source file content verbatim
- If the input was a description: use the draft content confirmed in Phase 1

---

## Phase 5 — Update all metadata

**5a. plugin.json** — `$REPO/plugins/design/.claude-plugin/plugin.json`

Read the current file. Add `"./skills/<skill-name>"` to the `skills` array. Bump the version: increment the MINOR version (e.g. `1.0.0` → `1.1.0`, `1.1.0` → `1.2.0`). Write the updated file.

**5b. marketplace.json** — `$REPO/.claude-plugin/marketplace.json`

Read the current file. Find the `design` entry in the `plugins` array. Add `"./skills/<skill-name>"` to its `skills` array. Update its `version` to match the version set in 5a. Write the updated file.

**5c. CHANGELOG.md** — `$REPO/plugins/design/CHANGELOG.md`

Prepend a new section at the top (after the header):

```markdown
## [<new-version>] - <today's date YYYY-MM-DD>

### Added
- `<skill-name>` skill — <description>

```

**5d. README.md** — `$REPO/plugins/design/README.md`

Add a new skill section following the existing pattern. Insert it in the `## Skills` section, before the `## Getting help` section, separated from other skills by a `---` rule:

```markdown
### `/design:<skill-name>` — <description>

<One paragraph describing what this skill does and when to use it.>

**How to use it:**

1. Type `/design:<skill-name>` and press `Enter`
2. <Describe what to type or provide as input>
3. Press `Enter` and Claude will <describe the output>

---
```

If the number of skills grows large enough to warrant grouping (e.g. 6+), consider proposing a restructure into themed sections (`### Copy & writing`, `### Design systems`, `### Contribution tools`) as part of the PR.

---

## Phase 6 — Commit and open a draft PR

Stage and commit:

```bash
cd "$REPO"
git add plugins/design/ .claude-plugin/marketplace.json
git commit -m "feat: add <skill-name> skill"
```

Push and open a draft PR:

```bash
git push -u origin add/<skill-name>
gh pr create --draft \
  --title "feat: add <skill-name> skill" \
  --body "## What

Adds the \`<skill-name>\` skill to the \`design\` plugin.

**Skill:** \`<skill-name>\`
**Description:** <description>

## Why

<Ask the user before this step: 'One sentence: why is this skill useful for other designers?'>

## Checklist

- [x] SKILL.md written and validated
- [x] plugin.json updated
- [x] marketplace.json updated
- [x] CHANGELOG.md updated
- [x] README.md updated"
```

Return the PR URL to the user.

**Done.** Tell them:

> "Your skill is ready for review. Share the PR link in `#design` so other designers can weigh in."

---

## Task

$ARGUMENTS
