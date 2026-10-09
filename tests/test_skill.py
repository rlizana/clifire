import os

import pytest

from clifire import application, skill
from tests.test_output import output


@pytest.fixture(autouse=True)
def reset_current_app():
    application.App.current_app = None
    yield


def test_skill_path_content():
    path = skill.path()
    assert os.path.exists(path)
    content = skill.content()
    assert content.startswith('---')
    assert 'name: clifire' in content


def test_skill_print(capsys):
    app = application.App()
    app.fire('skill print')
    printed = output(capsys)
    assert 'name: clifire' in printed


def test_skill_path_command(capsys):
    app = application.App()
    app.fire('skill path')
    printed = output(capsys)
    assert printed.strip() == skill.path()


def test_skill_install_all(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)
    app = application.App()
    app.fire('skill install --target all')
    expected = [
        '.claude/skills/clifire/SKILL.md',
        '.config/crush/skills/clifire/SKILL.md',
        '.agents/skills/clifire/SKILL.md',
        '.claude/skills/clifire/SKILL.md',
    ]
    for relative in expected:
        assert (tmp_path / relative).exists()
    printed = output(capsys)
    assert 'Installed skill file at' in printed


def test_skill_install_project(tmp_path, monkeypatch):
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)
    app = application.App()
    app.fire('skill install --target project')
    assert (tmp_path / '.claude/skills/clifire/SKILL.md').exists()
    assert (tmp_path / '.agents/skills/clifire/SKILL.md').exists()
    assert not (tmp_path / '.config/crush/skills/clifire/SKILL.md').exists()


def test_skill_install_auto_fallback(tmp_path, monkeypatch):
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)
    app = application.App()
    app.fire('skill install')
    assert (tmp_path / '.claude/skills/clifire/SKILL.md').exists()
    assert (tmp_path / '.config/crush/skills/clifire/SKILL.md').exists()
    assert not (tmp_path / '.agents/skills/clifire/SKILL.md').exists()


def test_skill_install_auto_existing_dir(tmp_path, monkeypatch):
    monkeypatch.setenv('HOME', str(tmp_path))
    monkeypatch.chdir(tmp_path)
    (tmp_path / '.claude').mkdir()
    app = application.App()
    app.fire('skill install')
    assert (tmp_path / '.claude/skills/clifire/SKILL.md').exists()
    assert not (tmp_path / '.config/crush/skills/clifire/SKILL.md').exists()


def test_skill_invalid_target(capsys):
    app = application.App()
    with pytest.raises(SystemExit) as excinfo:
        app.fire('skill install --target nope')
    assert excinfo.value.code == 40
    printed = output(capsys)
    assert 'The option "target" has an invalid value "nope"' in printed


def test_skill_invalid_action(capsys):
    app = application.App()
    with pytest.raises(SystemExit) as excinfo:
        app.fire('skill bogus')
    assert excinfo.value.code == 40
    printed = output(capsys)
    assert 'The argument "action" has an invalid value "bogus"' in printed
