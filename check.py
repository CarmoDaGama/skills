#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IGNORED = {'synced', '.git', '.vscode'}
SHARED = [
    ('img2html/scripts/snap.py', 'video2html/scripts/snap.py'),
    ('img2html/scripts/compare.py', 'video2html/scripts/compare.py'),
]


def frontmatter_name(text: str) -> str | None:
    m = re.match(r'---\r?\n(.*?)\r?\n---', text, re.S)
    if not m:
        return None
    name = re.search(r'^name:\s*(.+?)\s*$', m.group(1), re.M)
    return name.group(1).strip('"\'') if name else None


def main() -> int:
    errors: list[str] = []
    skills = sorted(p.parent.name for p in ROOT.glob('*/SKILL.md') if p.parent.name not in IGNORED)
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    linked = set(re.findall(r'\]\(\./([^)/]+)/?\)', readme))

    for skill in skills:
        name = frontmatter_name((ROOT / skill / 'SKILL.md').read_text(encoding='utf-8'))
        if name != skill:
            errors.append(f'{skill}: SKILL.md name is {name!r}, expected {skill!r}')
        yaml = ROOT / skill / 'agents' / 'openai.yaml'
        if not yaml.is_file():
            errors.append(f'{skill}: missing agents/openai.yaml')
        else:
            prompt = re.search(r'^\s*default_prompt:\s*"?Use \$([a-z0-9-]+)', yaml.read_text(encoding='utf-8'), re.M)
            if not prompt:
                errors.append(f'{skill}: openai.yaml has no default_prompt starting with "Use ${skill}"')
            elif prompt.group(1) != skill:
                errors.append(f'{skill}: openai.yaml default_prompt uses ${prompt.group(1)}')
            if 'allow_implicit_invocation' not in yaml.read_text(encoding='utf-8'):
                errors.append(f'{skill}: openai.yaml has no policy.allow_implicit_invocation')
        if skill not in linked:
            errors.append(f'{skill}: not listed in README.md')

    for missing in sorted(linked - set(skills)):
        errors.append(f'README.md lists ./{missing}, which has no SKILL.md')

    for copy, source in SHARED:
        a, b = ROOT / copy, ROOT / source
        if not a.is_file() or not b.is_file():
            errors.append(f'shared script missing: {copy if not a.is_file() else source}')
        elif a.read_bytes() != b.read_bytes():
            errors.append(f'{copy} differs from {source}: copy one over the other')

    if errors:
        print(f'check failed ({len(errors)}):')
        for error in errors:
            print(f'- {error}')
        return 1
    print(f'check passed: {len(skills)} skills, {len(SHARED)} shared scripts.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
