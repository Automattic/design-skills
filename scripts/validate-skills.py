"""Check the public marketplace, skill metadata, and local Markdown links."""

import argparse
import json
import re
from pathlib import Path

import yaml


def validate(root, tag=None):
    plugin = root / 'plugins' / 'a8c-design'
    manifest = json.loads((plugin / '.claude-plugin' / 'plugin.json').read_text())
    marketplace = json.loads((root / '.claude-plugin' / 'marketplace.json').read_text())
    entry, = marketplace['plugins']
    if entry['name'] != manifest['name'] or entry['source'] != './plugins/a8c-design':
        raise ValueError('Marketplace entry must point to the a8c-design plugin.')
    if entry['version'] != manifest['version'] or entry['skills'] != manifest['skills']:
        raise ValueError('Marketplace and plugin versions and skill lists must match.')
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?', manifest['version']):
        raise ValueError('Plugin version must use major.minor.patch, with an optional prerelease.')
    if tag is not None and tag != f'v{manifest["version"]}':
        raise ValueError(f'Release tag must be v{manifest["version"]}.')

    declared = manifest['skills']
    actual = {f'./skills/{folder.name}' for folder in (plugin / 'skills').iterdir() if folder.is_dir()}
    if len(set(declared)) != len(declared) or set(declared) != actual:
        raise ValueError('Manifest must list each skill folder exactly once.')

    for relative_path in declared:
        folder = plugin / relative_path
        if folder.is_symlink() or folder.resolve().parent != (plugin / 'skills').resolve():
            raise ValueError(f'Skill must be inside the skills folder: {relative_path}')
        if any(file.is_symlink() for file in folder.rglob('*')):
            raise ValueError(f'Review linked files before exporting {folder.name}.')
        content = (folder / 'SKILL.md').read_text()
        sections = re.fullmatch(r'---\r?\n(.*?)\r?\n---\r?\n(.*)', content, re.DOTALL)
        if sections is None or not sections[2].strip():
            raise ValueError(f'{folder.name} needs YAML frontmatter and instructions.')
        metadata = yaml.safe_load(sections[1])
        if not isinstance(metadata, dict):
            raise ValueError(f'Invalid frontmatter in {folder.name}.')
        name = metadata.get('name')
        if name != folder.name or len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            raise ValueError(f'Skill name must be kebab-case and match its folder: {folder.name}')
        description = metadata.get('description')
        if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
            raise ValueError(f'{folder.name} needs a description of 1–1024 characters.')

    for file in root.rglob('*.md'):
        if '.git' in file.relative_to(root).parts or 'dist' in file.relative_to(root).parts:
            continue
        for destination in re.findall(r'\]\(([^)]+)\)', file.read_text()):
            if re.match(r'^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|#|//)', destination):
                continue
            target = destination.split('#')[0]
            if not (file.parent / target).exists():
                raise ValueError(f'Missing local link in {file.relative_to(root)}: {destination}')
    print(f'Validated {len(declared)} skills and version {manifest["version"]}.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--tag', help='Require a matching v-prefixed release tag.')
    args = parser.parse_args()
    try:
        validate(args.root.resolve(), args.tag)
    except (ValueError, KeyError, TypeError, OSError, yaml.YAMLError) as error:
        parser.exit(1, f'Validation failed: {error}\n')


if __name__ == '__main__':
    main()
