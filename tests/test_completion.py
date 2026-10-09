import shutil
import subprocess

import pytest

from clifire import application
from clifire.commands import completion
from tests.test_output import output


@pytest.fixture(autouse=True)
def reset_current_app():
    application.App.current_app = None
    yield


def test_bash_script():
    app = application.App()
    script = completion.bash_script(app, 'fire')
    assert 'complete -F _clifire_completion fire' in script
    assert 'for cmd in ' in script
    assert 'help' in script
    assert 'completion' in script
    assert "cmd_opts['completion']" in script
    assert '--install' in script


def test_zsh_script():
    app = application.App()
    script = completion.zsh_script(app, 'myapp')
    assert script.startswith('#compdef myapp')
    assert 'compdef _clifire_completion myapp' in script
    assert 'help' in script
    assert '--no-ansi' in script


def test_fish_script():
    app = application.App()
    script = completion.fish_script(app, 'fire')
    assert script.startswith('# fish completion for fire')
    assert '__fish_use_subcommand' in script
    assert "-a 'completion'" in script
    assert '-l install' in script


def test_bash_syntax(tmp_path):
    if not shutil.which('bash'):
        pytest.skip('bash not available')
    app = application.App()
    script = completion.bash_script(app, 'fire')
    file = tmp_path / 'completion.bash'
    file.write_text(script)
    subprocess.run(['bash', '-n', str(file)], check=True)


def test_zsh_syntax(tmp_path):
    if not shutil.which('zsh'):
        pytest.skip('zsh not available')
    app = application.App()
    script = completion.zsh_script(app, 'fire')
    file = tmp_path / 'completion.zsh'
    file.write_text(script)
    subprocess.run(['zsh', '-n', str(file)], check=True)


def test_fish_syntax(tmp_path):
    if not shutil.which('fish'):
        pytest.skip('fish not available')
    app = application.App()
    script = completion.fish_script(app, 'fire')
    file = tmp_path / 'completion.fish'
    file.write_text(script)
    subprocess.run(['fish', '-n', str(file)], check=True)


def test_fire_completion_print(capsys):
    app = application.App()
    app.fire('completion bash')
    printed = output(capsys)
    assert 'complete -F _clifire_completion' in printed
    app = application.App()
    app.fire('completion zsh')
    printed = output(capsys)
    assert '#compdef fire' in printed


def test_completion_missing_shell(capsys):
    app = application.App()
    with pytest.raises(SystemExit) as excinfo:
        app.fire('completion')
    assert excinfo.value.code == 40
    printed = output(capsys)
    assert 'is required, choose bash, zsh or fish' in printed


def test_completion_invalid_shell(capsys):
    app = application.App()
    with pytest.raises(SystemExit) as excinfo:
        app.fire('completion powershell')
    assert excinfo.value.code == 40
    printed = output(capsys)
    assert 'has an invalid value "powershell"' in printed


def test_completion_install_zsh(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.setenv('SHELL', '/bin/zsh')
    app = application.App()
    app.fire('completion --install')
    dest = tmp_path / '.config/clifire/completion.zsh'
    assert dest.exists()
    assert '#compdef fire' in dest.read_text()
    rc_file = tmp_path / '.zshrc'
    assert 'source' in rc_file.read_text()
    printed = output(capsys)
    assert 'Completion script installed at' in printed
    app = application.App()
    app.fire('completion --install')
    assert rc_file.read_text().count('source') == 1


def test_completion_install_fish(tmp_path, monkeypatch):
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.setenv('SHELL', '/usr/bin/fish')
    app = application.App()
    app.fire('completion --install')
    dest = tmp_path / '.config/fish/completions/fire.fish'
    assert dest.exists()
    assert not (tmp_path / '.config/clifire').exists()


def test_completion_install_bash(tmp_path, monkeypatch):
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.setenv('SHELL', '/bin/bash')
    app = application.App()
    app.fire('completion --install --bin myapp')
    dest = tmp_path / '.config/clifire/completion.bash'
    assert dest.exists()
    assert 'complete -F _clifire_completion myapp' in dest.read_text()
    rc_file = tmp_path / '.bashrc'
    assert f'source {dest}' in rc_file.read_text()
