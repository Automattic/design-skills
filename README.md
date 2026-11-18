# Design Skills

Reusable design skills maintained by Automattic. Each skill includes instructions in `SKILL.md` and the files needed to follow them.

| Skill | Purpose | Requirements |
| --- | --- | --- |
| [jtbd-copy](plugins/a8c-design/skills/jtbd-copy/SKILL.md) | Review and rewrite copy through a Jobs to Be Done lens | User-provided copy or a flow description |
| [design-mockups](plugins/a8c-design/skills/design-mockups/SKILL.md) | Explore HTML/CSS designs in a local gallery | File access, a terminal, Node.js 20+, npm, and a browser |
| [wordpress-mockups](plugins/a8c-design/skills/wordpress-mockups/SKILL.md) | Build WordPress UI mockups using bundled tokens, icons, and components | Ability to read the bundled files and create HTML |

## Install

Use the instructions for your agent in the [plugin README](plugins/a8c-design/README.md). The skill folders use the [Agent Skills format](https://agentskills.io/specification). Each agent needs the capabilities listed above to complete the workflow.

For Claude Code, run these commands inside a session.

```text
/plugin marketplace add Automattic/design-skills
/plugin install a8c-design@design-skills
```

## Maintenance and contributions

Automattic maintains the source skills and any public replacements in its internal plugin repository. Maintainers prepare and review public exports before updating this repository. The internal export automation still needs to be configured.

To suggest an improvement or contribute a skill, [open an issue](https://github.com/Automattic/design-skills/issues) or follow [CONTRIBUTING.md](CONTRIBUTING.md). Maintainers bring accepted skill changes into the internal source and include them in a public export.

## License

[GPL-2.0-only](LICENSE)
