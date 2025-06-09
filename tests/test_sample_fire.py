import getpass
import importlib
import sys

from clifire import application
from tests.test_output import output


def get_app():
    module_name = "tests.sample.fire"
    if module_name in sys.modules:
        del sys.modules[module_name]
    app = application.App()
    importlib.import_module(module_name)
    return app


def test_fire_command(capsys):
    app = get_app()
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


def test_fire_without_doc(capsys):
    app = get_app()
    app.fire("nodoc")
    assert "Command without doc" in output(capsys)
