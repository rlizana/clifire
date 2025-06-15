import os
import subprocess
from unittest.mock import patch

import pytest

from clifire import application, out


def output(capsys):
    captured = capsys.readouterr()
    return out.ansi_clean(captured.out)


def test_app_no_command_provided(capsys):
    app = application.App(command_help=None)
    with pytest.raises(SystemExit) as excinfo:
        app.fire("")
    assert "10" == str(excinfo.value)
    assert "No command provided." in output(capsys)


def test_shell():
    app = application.App()
    res = app.shell("pwd")
    assert res.stdout in __file__

    path = os.path.dirname(__file__)
    assert os.getcwd() != path
    res = app.shell("pwd", path=path)
    assert res.stdout == path

    res = app.shell("echo $MY_ENV_VALUE", env={"MY_ENV_VALUE": "is_ok!"})
    assert "is_ok!" in res.stdout

    res = app.shell("this command not exist!")
    assert not res.stdout
    assert res.stderr


def test_shell_called_process_error():
    app = application.App()
    with patch("subprocess.run") as mocked_run:
        error = subprocess.CalledProcessError(
            returncode=1, cmd="dummy", stderr=b"error occurred"
        )
        mocked_run.side_effect = error

        res = app.shell("dummy")
        assert isinstance(res, application.result.ResultError)
        assert res.code == 1
        assert "error occurred" in res.stderr


def test_path():
    assert application.App.path("/tmp") == "/tmp"

    app = application.App()
    assert app.path("/tmp") == "/tmp"
    assert app.path("/tmp", "test", "file.txt") == "/tmp/test/file.txt"

    home = os.path.expanduser("~")
    assert app.path("~/test.txt") == os.path.join(home, "test.txt")
    assert app.path("./test") == os.path.abspath("./test")
    assert app.path("/tmp/my folder/file.txt") == "/tmp/my folder/file.txt"
    assert app.path("~/folder1", "folder2", "file.txt") == os.path.join(
        home, "folder1", "folder2", "file.txt"
    )

    assert app.path() == os.getcwd()
