# a8c-design

Portable design workflows maintained by Automattic. The `skills/` folder contains seven skills and their supporting files.

| Skill | What it does | Example request |
| --- | --- | --- |
| [jtbd-copy](skills/jtbd-copy/SKILL.md) | Review and rewrite copy through a Jobs to Be Done lens | Review the labels and button text in this onboarding flow. |
| [design-mockups](skills/design-mockups/SKILL.md) | Explore visual directions and compare HTML/CSS mockups in a gallery | Explore three visual directions for my portfolio. |
| [wordpress-mockups](skills/wordpress-mockups/SKILL.md) | Compose WordPress UI using bundled tokens, 321 icons, 12 components, and layout patterns | Mock up a Site Editor sidebar for managing design tokens. |
| [design-tokens](skills/design-tokens/SKILL.md) | Create and validate design token systems and themes | Create primitive and semantic tokens for light and dark themes. |
| [voiceover-scriptwriting](skills/voiceover-scriptwriting/SKILL.md) | Draft, normalize, and time spoken narration | Write a thirty-second product explainer for small business owners. |
| [wpds-changes](skills/wpds-changes/SKILL.md) | Summarize changes and discussions in the WordPress design system | Summarize WordPress design system updates from the last week. |
| [feedback-triage](skills/feedback-triage/SKILL.md) | Turn a call or review into a page where you decide on every point, then build the approved ones | Triage the transcript from yesterday's design review. |

## Claude Code

Run these commands in a Claude Code session.

```text
/plugin marketplace add Automattic/design-skills
/plugin install a8c-design@design-skills
```

Invoke `/a8c-design:<skill-name>`, followed by your request. For example, use `/a8c-design:voiceover-scriptwriting` or `/a8c-design:wpds-changes week`. The plugin makes all seven skills available.

## Codex

Clone or download this repository. Copy the complete folders for the skills you want from `plugins/a8c-design/skills/` into your project's `.agents/skills/` directory, or into `~/.agents/skills/` for personal use across projects. Keep their supporting files together. Invoke a skill by name, for example `$jtbd-copy`, and provide your request.

## ChatGPT

On accounts with skill uploading available, open **Plugins → Skills → Create → Upload from your computer** and upload one skill ZIP.

Use an individual skill archive from [GitHub Releases](https://github.com/Automattic/design-skills/releases), when available. To build an archive from a downloaded checkout, run `python3 scripts/package-skills.py` from the repository root, then select the appropriate ZIP in `dist/`.

Availability depends on the account and workspace settings. See [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

`jtbd-copy` works with user-provided text. `wordpress-mockups` requires access to its bundled files and a way to create HTML. `design-mockups` requires a terminal, Node.js 20+, npm, and a reachable browser preview. `feedback-triage` needs Python to render its page and a way to give you the HTML file. Check that your ChatGPT environment provides those capabilities before using it.

## Other agents

Install the complete skill folder using your agent's Agent Skills instructions. If the agent accepts instructions and attachments manually, provide `SKILL.md` and the supporting files it needs. Check the agent's support for scripts and file access.

## Requirements

For `design-mockups`, use a development environment with Node.js 20+, npm, filesystem access, and a browser. The skill includes an Express server template and setup commands. Preview URLs are local to the machine running the server. For a remote environment, use its browser preview or port forwarding feature.

For `wordpress-mockups`, retain `base.css`, `tokens/`, `icons/`, `components/`, and `patterns/` with `SKILL.md`. File paths in the instructions are relative to the installed skill folder.

For `design-tokens`, retain `assets/`, `references/`, and `scripts/`. Its validator uses Python 3. Optional token builds require Node.js/npm and the packages described in `references/build-tools.md`.

For `voiceover-scriptwriting`, retain `references/` and `scripts/`. The bundled duration check requires Python 3.10+. The skill supports estimating duration when code execution is unavailable. Audio generation is optional and requires access to the chosen provider.

For `wpds-changes`, provide the timespan in your request. The source instructions refer to Claude tool names such as `AskUserQuestion`, `Bash`, and `WebSearch`. In other agents, use their equivalent question, date, and web/GitHub search capabilities. It reads public WordPress repositories.

For `feedback-triage`, retain `assets/`, `references/`, and `scripts/`. Rendering the triage page uses Python 3. In Claude Code signed in to claude.ai, the page is published as an Artifact with a shared store: decisions save as they're made and progress appears live. Elsewhere, the page is a self-contained HTML file to open in a browser. Choices stay in that browser until **Copy decisions** or **Download** hands them back, and the agent re-renders the page to show progress. Building the approved items needs a repository, git, and optionally `gh` for pull requests. The instructions use Claude tool names such as `Artifact`, `ArtifactData`, and `AskUserQuestion`; other agents use the local-file path and their own question tool.

The internal `product-jtbd-copy` workflow is available here as `jtbd-copy`, keeping the existing public skill name.

## Credits and maintenance

The mockup skills were contributed by Shaun Andrews and ported from [shaunandrews/agent-skills](https://github.com/shaunandrews/agent-skills).

Maintainers prepare skill updates and public replacements in the internal source before exporting them here. See [CONTRIBUTING.md](../../CONTRIBUTING.md) for suggestions and bug reports.
