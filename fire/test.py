from clifire import command


@command.fire
def test_legacy(cmd, _build: bool = False, python_version: str = '3.8.2'):
    '''
    Launch tests in docker image with specified Python version

    Args:
        python_version: Python version to use for the tests. (default: '3.8.2')
        _build: Force build the Docker image before running tests.
    '''

    image_name = f'clifire-py{python_version}'

    def docker_build():
        cmd.app.shell(
            f'docker build --build-arg PYTHON_VERSION={python_version} '
            f'-t {image_name} .',
            capture_output=False,
        )

    if _build:
        docker_build()
    elif image_name not in cmd.app.shell('docker images').stdout:
        docker_build()

    volumen_str = '-v ./src:/app/src -v ./tests:/app/tests'
    cmd.app.shell(
        f'docker run --rm {volumen_str} {image_name}',
        capture_output=False,
    )
