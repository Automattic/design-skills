# Design Plugin

AI skills for Automattic designers, bundled into a single Claude Code plugin.

> **Early version.** Four skills to start — contributing new skills, rewriting copy through a JTBD lens, prototyping HTML/CSS design mockups, and building WordPress/Gutenberg UI mockups. More coming soon.

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
   /plugin marketplace add Automattic/design-skills
   ```
5. Install the plugin:
   ```
   /plugin install design
   ```
6. Press `Enter` to choose **Install for you (user scope)**
7. Type `exit` and restart Claude Code
8. Type `/` in the chat input — you should see `/design:add-skill`, `/design:jtbd-copy`, `/design:design-mockups`, and `/design:wordpress-mockups` in the list

---

## Skills

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

### `/design:design-mockups` — Rapidly prototype HTML/CSS mockups with a local preview server

For when you want to explore multiple visual directions for a website or interface and compare them side by side. This skill sets up a local Express server with a gallery UI and walks you through three phases: style exploration (testing aesthetic directions), site templates (building out the chosen direction across pages), and section explorations (iterating on specific components).

Works best for website design, landing pages, and any project where you want to rapidly generate and present visual options.

**How to use it:**

1. Type `/design:design-mockups` and press `Enter`
2. Describe the project you want to mock up. Examples:
   ```
   I'm designing a personal portfolio site — help me explore 3 or 4 different style directions
   ```
   ```
   Build out the page templates for the "terminal-minimal" direction I picked
   ```
3. Claude will scaffold the project, spin up a local server, generate HTML mockups, and give you a gallery URL to review and iterate on

**What it handles:**

- Setting up a local Express server with gallery UI
- Generating standalone HTML/CSS mockups with embedded styles
- Organizing mockups into phases (exploration → templates → sections)
- Naming conventions for iterations and variants
- Restarting the server when files change

*Contributed by Shaun Andrews. Ported from [shaunandrews/agent-skills](https://github.com/shaunandrews/agent-skills).*

---

### `/design:wordpress-mockups` — Build accurate WordPress/Gutenberg UI mockups

For when you're designing new interfaces or features for WordPress admin, the Site Editor, or any Gutenberg-based UI. This skill ships with pre-extracted design tokens, 321 icons, 12 components, and layout patterns — all copied directly from the Gutenberg source — so mockups look and behave like the real thing from the first pixel.

Instead of hand-rolling styles, Claude composes your mockup from real WordPress primitives.

**How to use it:**

1. Type `/design:wordpress-mockups` and press `Enter`
2. Describe the UI you want to build. Examples:
   ```
   Mock up a new Site Editor sidebar panel for managing design tokens
   ```
   ```
   Build a modal for the block inserter with a new "AI suggestions" tab
   ```
3. Claude will check patterns first, compose components from the library, and return a self-contained HTML file with real WordPress tokens, icons, and markup

**What it handles:**

- WordPress design tokens (colors, spacing, typography, elevation, radii)
- 321 Gutenberg icons
- 12 core components (buttons, inputs, modals, panels, tabs, toolbars, etc.)
- Layout patterns (Site Editor header, etc.) with composition rules
- WordPress-accurate class naming and modifiers

*Contributed by Shaun Andrews. Ported from [shaunandrews/agent-skills](https://github.com/shaunandrews/agent-skills).*

---

## Getting help

- **Stuck on setup?** Ask in `#design` on Slack
- **Want to contribute?** See [CONTRIBUTING.md](../../CONTRIBUTING.md)
- **Found a bug?** Open an issue
