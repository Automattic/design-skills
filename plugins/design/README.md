# Design Plugin

AI skills for Automattic designers, bundled into a single Claude Code plugin.

> **Early version.** Two skills to start — one for rewriting copy through a JTBD lens, one for contributing new skills to this plugin. More coming soon.

---

## What is Claude Code?

Claude Code is a version of Claude that runs in your terminal and can take actions — read files, write code, call APIs, and more. It's different from the Claude chat interface because it can actually *do* things, not just suggest them. [Learn more](https://code.claude.com).

---

## Install

1. Open **Terminal** (press `Cmd + Space`, type `Terminal`, press `Enter`)
2. Install Claude Code if you haven't already:
   ```
   npm install -g @anthropic-ai/claude-code
   ```
3. Launch Claude Code:
   ```
   claude
   ```
4. Add this marketplace:
   ```
   /plugin marketplace add REPO_PLACEHOLDER
   ```
5. Install the plugin:
   ```
   /plugin install design
   ```
6. Press `Enter` to choose **Install for you (user scope)**
7. Type `exit` and restart Claude Code
8. Type `/` in the chat input — you should see `/design:jtbd-copy` and `/design:add-skill` in the list

---

## Skills

### `/design:jtbd-copy` — Rewrite any copy through a Jobs to Be Done lens

For when a form, landing page, email, or ad feels functional but cold — copy that describes the system or features instead of what the reader is actually trying to do. Paste in your copy and Claude will rewrite every element so the language reflects the reader's job, not the feature's structure.

Works for product UI, landing pages, marketing copy, emails, ads, onboarding, error states — anywhere copy lives.

**How to use it:**

1. Type `/design:jtbd-copy` and press `Enter`
2. Describe what you're working on, or paste in the copy directly. Examples:
   ```
   I'm working on the client invite flow. The button says "Submit" and the field is labeled "Custom message". Can you review it?
   ```
   ```
   Review this landing page hero: "AI-powered workflows for modern teams. Get started today."
   ```
3. Press `Enter` — Claude returns a full copy audit

**What you get back:**

- A one-sentence job statement: "The reader is trying to..."
- A before/after table for every element
- Flagged cognitive gaps — places where the reader might lose the thread
- A short rationale for each rewrite

**Example output:**

```
Job: "Get my client set up so they can start using the product"

| Element     | Current        | Proposed                          | Why                         |
|-------------|----------------|-----------------------------------|-----------------------------|
| Header      | (none)         | Send this to your client          | Frames the job              |
| Field label | Custom message | Personal note                     | User's language             |
| Helper text | (none)         | Builds trust, shows it's from you | Connects to the job         |
| Primary CTA | Submit         | Send to client                    | Names the outcome           |
```

---

### `/design:add-skill` — Add a new skill to the design plugin

Built a workflow you want to share with the design org? This skill walks you through contributing it end-to-end — from your SKILL.md file to an open draft PR. No git experience required.

**How to use it:**

1. Type `/design:add-skill` followed by a path to your SKILL.md, or describe what your skill does. Examples:
   ```
   /design:add-skill ~/my-skill/SKILL.md
   ```
   ```
   /design:add-skill I want to contribute a skill that reviews spacing in Figma exports
   ```
2. Press `Enter` — Claude will validate your skill, find the repo, create a branch, scaffold the files, update all metadata, and open a draft PR
3. Share the PR link in `#design` so other designers can weigh in

**What it handles:**

- Validating your skill's frontmatter and structure
- Finding (or cloning) the repo
- Creating a branch from latest `main`
- Writing your skill to the right directory
- Updating `plugin.json`, `marketplace.json`, `CHANGELOG.md`, and `README.md`
- Opening a draft PR

---

## Getting help

- **Stuck on setup?** Ask in `#design` on Slack
- **Want to contribute?** See [CONTRIBUTING.md](../../CONTRIBUTING.md)
- **Found a bug?** Open an issue
