# Contributing to Design Skills

Thanks for wanting to contribute. This repo hosts the `design` plugin — a collection of AI skills for Automattic designers.

## Fast path — use the `/design:add-skill` workflow

If you have the plugin installed, the fastest way to contribute a skill is:

```
/design:add-skill path/to/your/SKILL.md
```

It will find the repo, create a branch, scaffold your skill, update all metadata, and open a draft PR for you.

## Manual path

1. Fork the repo and clone your fork
2. Create a branch: `git checkout -b add/<your-skill-name>`
3. Create your skill directory at `plugins/design/skills/<your-skill-name>/`
4. Add a `SKILL.md` file with YAML frontmatter:

   ```markdown
   ---
   name: your-skill-name
   description: When and why to use this skill
   argument-hint: "[what to pass as input]"
   ---

   # Your Skill Title

   Skill content here.

   ## Task

   $ARGUMENTS
   ```

5. Update `plugins/design/.claude-plugin/plugin.json`:
   - Add `"./skills/<your-skill-name>"` to the `skills` array
   - Bump the minor version (e.g. `1.0.0` → `1.1.0`)
6. Update `.claude-plugin/marketplace.json`:
   - Find the `design` plugin entry
   - Add `"./skills/<your-skill-name>"` to its `skills` array
   - Match the version from `plugin.json`
7. Update `plugins/design/CHANGELOG.md`:
   - Prepend a new section at the top with the new version and today's date
8. Update `plugins/design/README.md`:
   - Add a new section for your skill
9. Commit: `git commit -m "feat: add <skill-name> skill"`
10. Push and open a draft PR

## Rules

- **Naming**: skill directories and the `name:` field must be kebab-case (lowercase letters, digits, hyphens only)
- **Description**: must be a clear one-liner describing when the skill should activate
- **Content**: no internal URLs, no private resources, no credentials, no examples that leak private context
- **License**: contributions are GPL-2.0, matching the repo

## Questions

Open an issue or ask in `#design` on Slack.
