import os
import stat

from clifire import command, out


@command.fire
def install(cmd, _global: False):
    '''
    Install global `fire` command

    Args:
    global: Install the command globally
    '''
    install_path = cmd.app.path('~/.local/bin')
    if not os.path.exists(install_path):
        out.debug2(f'Install path {install_path} not exist')
        install_path = cmd.app.path('/usr/local/bin')
    if not os.path.exists(install_path):
        out.debug2(f'Install path {install_path} not exist')
        out.critical('No path for install')
    fire_path = f'{install_path}/fire'
    out.info(f'Command available at {fire_path}')
    pyproject_path = cmd.app.path('pyproject.toml')
    with open(fire_path, 'w') as fp:
        fp.write(
            '\n'.join(
                [
                    '#!/bin/bash',
                    f'rye run --pyproject {pyproject_path} fire "$@"',
                ]
            )
        )
    os.chmod(
        fire_path,
        stat.S_IRWXU
        | stat.S_IRGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH,
    )
    out.success('Installation completed!')


@command.fire
def build(cmd):
    '''
    Build the package and documentation
    '''
    live = out.LiveText('Building ...')
    res = cmd.app.shell('rye build')
    if res:
        live.success('Build success')
    else:
        live.error('Error on building packages.')
        out.error(res.stderr)
        return 1

    live.info('Building the docs ..')
    cmd.app.fire('doc build')


@command.fire
def coverage(cmd):
    '''
    Launch tests with coverage
    '''
    bash = 'rye run coverage run -m pytest && rye run coverage html'
    cmd.app.shell(bash, capture_output=False)


@command.fire
def precommit(cmd):
    '''
    Launch pre-commit
    '''
    cmd.app.shell('pre-commit run --all-files', capture_output=False)
