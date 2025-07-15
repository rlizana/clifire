from clifire import command


@command.fire
def test_legacy(cmd, _build: bool = False):
    '''
    Launch tests in docker image with Python 3.8.2
    '''

    def docker_build():
        cmd.app.shell(
            'docker build -t clifire-py38-tests .', capture_output=False
        )

    if _build:
        docker_build()
    elif 'clifire-py38-tests' not in cmd.app.shell('docker images').stdout:
        docker_build()
    volumen_str = '-v ./src:/app/src -v ./tests:/app/tests'
    cmd.app.shell(
        f'docker run --rm {volumen_str} clifire-py38-tests',
        capture_output=False,
    )
