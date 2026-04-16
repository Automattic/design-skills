# Changelog

All notable changes to the `a8c-design` plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-04-16

### Added
- `wordpress-librarian` skill — investigates what decisions on WordPress were made and generates a summary document indicating the main conclusions and insights

## [2.0.0] - 2026-04-10

### Changed

- **Breaking:** renamed plugin from `design` to `a8c-design`. All slash commands are now `/a8c-design:<skill>` (e.g. `/a8c-design:add-skill`, `/a8c-design:jtbd-copy`, `/a8c-design:design-mockups`, `/a8c-design:wordpress-mockups`). Reinstall with `/plugin install a8c-design`.

## [1.1.0] - 2026-04-10

### Added

- `design-mockups` skill — rapidly prototype and present HTML/CSS design mockups with a local preview server, organized into style exploration, site templates, and section iteration phases (contributed by Shaun Andrews, ported from [shaunandrews/agent-skills](https://github.com/shaunandrews/agent-skills))
- `wordpress-mockups` skill — build accurate WordPress/Gutenberg UI mockups using pre-extracted design tokens, 321 icons, 12 components, and site editor patterns (contributed by Shaun Andrews, ported from [shaunandrews/agent-skills](https://github.com/shaunandrews/agent-skills))

## [1.0.0] - 2026-04-10

### Added

- `jtbd-copy` skill — rewrite any copy (product UI, landing pages, marketing, emails) through a Jobs to Be Done lens
- `add-skill` skill — guided contribution workflow for adding new skills to this plugin
