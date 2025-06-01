import os
import subprocess
from unittest.mock import patch

from clifire import application, result


def test_result():
    res = result.Result(0, "OK", "KO")
    assert bool(res) is True
    assert res.code == 0
    assert str(res)
    assert str(res) == res.__repr__()

    res = result.ResultOk("OK")
    assert bool(res) is True
    assert res.code == 0
    assert res.stdout == ["OK"]
    assert res.stderr == ""

    res = result.ResultError("ERROR", 99)
    assert bool(res) is False
    assert res.code == 99
    assert res.stdout == ""
    assert res.stderr == ["ERROR"]


def test_shell():
    app = application.App()
    res = app.shell("pwd")
    assert res.stdout[0] in __file__

    path = os.path.dirname(__file__)
    assert os.getcwd() != path
    res = app.shell("pwd", path=path)
    assert res.stdout[0] == path

    res = app.shell("echo $MY_ENV_VALUE", env={"MY_ENV_VALUE": "is_ok!"})
    assert "is_ok!" in res.stdout[0]

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
