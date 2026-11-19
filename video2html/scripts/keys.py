from __future__ import annotations

import os
import re
import sys
from pathlib import Path


def key(name: str) -> str:
    if os.environ.get(name):
        return os.environ[name]
    pattern = re.compile(rf'^\s*(?:export\s+)?{re.escape(name)}\s*=\s*(.*?)\s*$')
    for env in (Path.cwd() / '.env', Path.home() / '.env'):
        if not env.is_file():
            continue
        for line in env.read_text(encoding='utf-8').splitlines():
            m = pattern.match(line)
            if m and m.group(1):
                return m.group(1).strip('"').strip("'")
    sys.exit(f'ERROR: set {name} (environment, .env or ~/.env).')
