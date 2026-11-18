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

Pull requests and updates to `trunk` run the public skill checks and build downloadable ZIPs under the workflow's `skill-downloads` artifact. These checks cover matching skill names, required metadata, manifest consistency, and local Markdown links.

To run the checks locally, install `scripts/requirements.txt` in a Python virtual environment, then run `python scripts/validate-skills.py`.

To build individual skill ZIPs from a reviewed checkout, run `python3 scripts/package-skills.py`. The archives are written to `dist/`. Each archive contains the complete skill folder and a copy of the repository license. Attach those ZIPs to the corresponding GitHub release. Rebuild them for each release so every download uses the same published skill files.


## Prepare a GitHub release

1. Merge the reviewed public export. Match the plugin and marketplace entry versions and update the changelog.
2. Create a tag such as `v2.0.1` on that commit and push it to GitHub.
3. Open **Actions → Prepare skill release → Run workflow** and enter that tag. Run the workflow from `trunk`.
4. The workflow checks the tagged files and version, builds the ZIPs, and attaches them to a draft release. Review the draft and downloads, then publish it.

The workflow requires an existing tag and a matching version. You can rerun it to replace the ZIPs on the same draft. Prepare a new version for changes after publication. The internal export into this repository is configured separately in the internal source repository.
