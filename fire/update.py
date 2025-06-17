import re

from clifire import command, out


@command.fire
def update_version(cmd):
    '''
    Update the clifire version according to pyproject.toml
    '''
    pyproject_path = cmd.app.path('pyproject.toml')
    with open(pyproject_path) as f:
        content = f.read()
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if match is None:
        out.critical(f'Version not detected {pyproject_path}')
    version = match.group(1)
    out.debug(f'Version "{version}" in {pyproject_path}')
    with open(cmd.app.path('src/clifire/main.py')) as f:
        content = f.read()
    new_content = re.sub(
        r'app = application\.App\('
        r'name=["\'"]CliFire["\'], '
        r'version=["\'"][^\'"]+["\']\)',
        f'app = application.App(name=\'CliFire\', version=\'{version}\')',
        content,
    )
    if new_content != content:
        with open(cmd.app.path('src/clifire/main.py'), 'w') as f:
            f.write(new_content)
        out.success(f'Update the version to {version}')
    else:
        out.warn(f'The version is correct, version {version}')
