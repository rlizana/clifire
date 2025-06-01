import runpy
import sys

from clifire import out
from tests.sample.out import app


def output(capsys):
    captured = capsys.readouterr()
    return out.ansi_clean(captured.out)


def test_main_block(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["tests/sample/out.py", "help info"])
    runpy.run_module("tests.sample.out", run_name="__main__")
    assert "Show a message text with info style." in output(capsys)


def test_sample_out_info(capsys):
    app.launch("help info")
    printed = output(capsys)
    assert "Show a message text with info style." in printed
    assert "Message text to show " in printed
    assert "A sample name " in printed
    assert " -t " in printed
    assert "--color" in printed

    app.launch('info "Hello World"')
    printed = output(capsys)
    assert "Hello World" in printed

    app.launch('info "Hello World" --type warn')
    printed = output(capsys)
    assert "Hello World" in printed

    app.launch('info "Hello World" --type error')
    printed = output(capsys)
    assert "Hello World" in printed

    app.launch('info "Hello World" --type not-exists')
    printed = output(capsys)
    assert 'Type "not-exists" unknow' in printed

    app.launch('info "Hello World" Elvis --type warn')
    printed = output(capsys)
    assert "Elvis: Hello World" in printed


def test_sample_out_info_ask(capsys):
    app.launch("help info ask")
    printed = output(capsys)
    assert "Show a message text like a question." in printed
    assert " -t " in printed
    assert "--color" in printed
    assert "--char" in printed

    app.launch('info ask "Hello World"')
    printed = output(capsys)
    assert "Hello World?" in printed

    app.launch('info ask "Hello World" --type warn --char !')
    printed = output(capsys)
    assert "Hello World!" in printed

    app.launch('info ask "Hello World" --type error --end-char !')
    printed = output(capsys)
    assert "Hello World!" in printed

    app.launch('info ask "Hello World" --type not-exists --end-char !')
    printed = output(capsys)
    assert 'Type "not-exists" unknow' in printed


def test_sample_out_live(capsys):
    app.launch("live 2")
    printed = output(capsys)
    assert "Regresive count for 2 ended!" in printed
