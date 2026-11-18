# Contributing to Design Skills

Use [GitHub issues](https://github.com/Automattic/design-skills/issues) for questions, bugs, and new skill suggestions. Include the skill name, the agent you used, your input, and what happened. Use examples you can share publicly.

You can also submit a pull request as a proposed change. Maintainers bring accepted skill changes into the internal source, update any public replacements there, and publish the result through a reviewed export. Public skill files are maintained through that process.

## Propose a change

1. Fork the repository and clone your fork.
2. Create a branch from `trunk`.
3. Make your proposed change under `plugins/a8c-design/skills/` and include any supporting files it needs.
4. Explain the problem and describe how you tried the skill in your pull request.

Maintainers handle release versions and generated metadata when preparing an export.

## Skill requirements

- Follow the [Agent Skills specification](https://agentskills.io/specification). Use a `SKILL.md` with `name` and `description` frontmatter. The name must match its folder.
- Write instructions that use the user's request as input. Describe required capabilities and dependencies clearly.
- Include templates, references, and other files needed to run the skill.
- Keep examples and resources suitable for public use. Exclude internal URLs, private context, and credentials.
- Keep Brand skills outside this collection.
- Contributions use GPL-2.0-only, matching the repository.

## Maintainer releases

Prepare skill changes in the internal source, including public replacement files and export rules. Review the resulting public files before pushing them here. Record the public changes in the plugin changelog and keep the marketplace entry and plugin versions aligned.

To build individual skill ZIPs from a reviewed checkout, run `python3 scripts/package-skills.py`. The archives are written to `dist/`. Each archive contains the complete skill folder and a copy of the repository license. Attach those ZIPs to the corresponding GitHub release. Rebuild them for each release so every download uses the same published skill files.
