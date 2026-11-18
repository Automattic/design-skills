"""Build one uploadable ZIP per public skill from the plugin manifest."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main():
    root = Path(__file__).resolve().parent.parent
    plugin = root / 'plugins' / 'a8c-design'
    manifest = json.loads((plugin / '.claude-plugin' / 'plugin.json').read_text())
    output = root / 'dist'
    output.mkdir(exist_ok=True)

    for relative_path in manifest['skills']:
        skill = plugin / relative_path
        if skill.is_symlink() or skill.resolve().parent != (plugin / 'skills').resolve():
            raise ValueError(f'Skill must be a folder inside skills/: {relative_path}')
        if not (skill / 'SKILL.md').is_file():
            raise ValueError(f'Missing SKILL.md: {relative_path}')
        files = sorted(skill.rglob('*'))
        if any(file.is_symlink() for file in files):
            raise ValueError(f'Review linked files before packaging {skill.name}')
        destination = output / f'{skill.name}-{manifest["version"]}.zip'
        with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
            for file in files:
                if file.is_file():
                    archive.write(file, Path(skill.name) / file.relative_to(skill))
            if not (skill / 'LICENSE').exists():
                archive.write(root / 'LICENSE', Path(skill.name) / 'LICENSE')
        print(destination.relative_to(root))


if __name__ == '__main__':
    main()
