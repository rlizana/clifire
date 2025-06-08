import getpass
import importlib

from clifire import application
from tests.test_output import output


def test_fire_command(capsys):
    app = application.App()
    importlib.import_module("tests.sample.fire")
    app.fire("hello Rob")
    assert "Hi Rob!" in output(capsys)
    app.fire("hello Rob -v")
    assert "Hi Rob!" in output(capsys)
    app.fire("hello -v Rob")
    assert "Hi Rob!" in output(capsys)
    app.fire("-v hello Rob")
    assert "Hi Rob!" in output(capsys)
    app.fire("hello")
    assert f"Hi {getpass.getuser()}!" in output(capsys)
    app.fire('hello "Rob Lizana"')
    printed = output(capsys)
    assert "Hi Rob Lizana!" in printed
    assert "Sudo = False" in printed
    app.fire('hello -v "Rob Lizana" --sudo')
    printed = output(capsys)
    assert "Hi Rob Lizana!" in printed
    assert "Sudo = True" in printed
