import getpass
import importlib
import os
import runpy
import sys
from contextlib import contextmanager

import pytest

from clifire import application, main
from tests.test_output import output


def get_app():
    module_name = "tests.sample.fire"
    if module_name in sys.modules:
        del sys.modules[module_name]
    app = application.App()
    importlib.import_module(module_name)
    return app


def test_main_block(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["clifire/main.py", "help"])
    if "clifire.main" in sys.modules:
        del sys.modules["clifire.main"]
    runpy.run_module("clifire.main", run_name="__main__")
    assert "Show this help" in output(capsys)


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


@contextmanager
def in_path(*args):
    cwd = os.getcwd()
    os.chdir(application.App.path(os.path.dirname(__file__), *args))
    try:
        yield
    finally:
        os.chdir(cwd)


def test_fire_main(capsys):
    with in_path("sample"):
        main.main("nodoc")
        assert "Command without doc" in output(capsys)


def test_fire_not_found_in_parents(capsys):
    temp_dir = os.getenv("TMPDIR") or "/tmp"
    assert os.path.isdir(temp_dir)
    with in_path(temp_dir):
        with pytest.raises(SystemExit):
            main.main("nodoc")
        assert "Command without doc" not in output(capsys)


def test_fire_find_file_py_in_parents(capsys):
    with in_path("sample", "parent"):
        main.main("nodoc")
        assert "Command without doc" in output(capsys)
    with in_path("sample", "parent_fire", "child"):
        main.main("nodoc")
        assert "Command without doc" in output(capsys)
    with in_path("sample", "parent_fire", "child", "grandson"):
        main.main("nodoc")
        assert "Command without doc" in output(capsys)


def test_fire_find_folder_in_parents(capsys):
    with in_path("sample", "parent_fire"):
        main.main("nodoc")
        assert "Command without doc" in output(capsys)
    with in_path("sample", "parent_fire", "child"):
        main.main("nodoc")
        assert "Command without doc" in output(capsys)
    with in_path("sample", "parent_fire", "child", "grandson"):
        main.main("nodoc")
        assert "Command without doc" in output(capsys)


def test_fire_group_help(capsys):
    app = get_app()

    app.fire("help")
    printed = output(capsys)
    assert "Available Commands:" in printed
    assert " cd " in printed
    assert " ef " in printed
    assert " ef gh " in printed
    assert "doc_ab_cd" in printed
    assert "doc_ab_ef_gh" in printed

    app.fire("help ab")
    printed = output(capsys)
    assert "Available Commands:" in printed
    assert "doc_ab" in printed
    assert "doc_ab_cd" in printed
    assert "ef gh" in printed
    assert "doc_ab_ef_gh" in printed

    app.fire("help ab ef")
    printed = output(capsys)
    assert "ab ef" not in printed
    assert "doc_ab_ef_gh" in printed

    app.fire("help zz")
    assert "Available Commands:" in output(capsys)

    app.fire("help zz command")
    assert "Available Commands:" not in output(capsys)

    app.fire("ab")
    assert "def_ab" in output(capsys)

    app.fire("ab cd")
    assert "def_ab_cd" in output(capsys)

    app.fire("ab ef gh")
    assert "def_ab_ef_gh" in output(capsys)

    app.fire("zz command")
    assert "def_zz_command" in output(capsys)
