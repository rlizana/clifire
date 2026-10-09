import os
import shutil
from typing import List

SKILL_NAME = 'clifire'


def path() -> str:
    folder = os.path.dirname(os.path.abspath(__file__))
    checkout = os.path.abspath(os.path.join(folder, '..', '..', 'SKILL.md'))
    if os.path.exists(checkout):
        return checkout
    return os.path.join(folder, 'SKILL.md')


def content() -> str:
    with open(path()) as file:
        return file.read()


def targets() -> dict:
    home = os.path.expanduser('~')
    cwd = os.getcwd()
    roots = {
        'claude': os.path.join(home, '.claude'),
        'crush': os.path.join(home, '.config', 'crush'),
        'project-claude': os.path.join(cwd, '.claude'),
        'project-agents': os.path.join(cwd, '.agents'),
    }
    return {
        name: os.path.join(root, 'skills', SKILL_NAME, 'SKILL.md')
        for name, root in roots.items()
    }


def _root(dest: str) -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(dest)))


def install(target: str = 'auto') -> List[str]:
    known = targets()
    if target == 'all':
        names = sorted(known)
    elif target == 'project':
        names = ['project-agents', 'project-claude']
    elif target in known:
        names = [target]
    elif target == 'auto':
        names = [
            name for name, dest in known.items() if os.path.exists(_root(dest))
        ]
        if not names:
            names = ['claude', 'crush']
    else:
        raise ValueError(f'Unknown skill target "{target}"')
    source = path()
    written = []
    for name in sorted(names):
        dest = known[name]
        if os.path.abspath(source) == os.path.abspath(dest):
            written.append(dest)
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(source, dest)
        written.append(dest)
    return written
