import time
from io import StringIO

import pytest
from clifire import application, out
from rich.console import Console


@pytest.fixture(autouse=True)
def reset_current_app():
    application.App.current_app = None
    yield


def output(capsys):
    captured = capsys.readouterr()
    return out.ansi_clean(captured.out)


def test_info(capsys):
    out.info('Info sample message')
    assert 'Info sample message\n' == output(capsys)


def test_success(capsys):
    out.success('Success sample message')
    assert 'Success sample message\n' == output(capsys)


def test_warn(capsys):
    out.warn('Warn sample message')
    assert 'Warn sample message\n' == output(capsys)


def test_error(capsys):
    out.warn('Error sample message')
    assert 'Error sample message\n' == output(capsys)


def test_critical(capsys):
    with pytest.raises(SystemExit) as excinfo:
        out.critical('Critical sample message 1')
    assert '1' == str(excinfo.value)
    assert 'Critical sample message 1\n' == output(capsys)
    with pytest.raises(SystemExit) as excinfo:
        out.critical('Critical sample message', 99)
    assert '99' == str(excinfo.value)
    assert 'Critical sample message\n' == output(capsys)


def test_debug(capsys):
    out.debug('Debug sample message')
    assert 'Debug sample message\n' == output(capsys)


def test_live_text():
    buffer = StringIO()
    original_console = out.CONSOLE
    try:
        out.CONSOLE = Console(
            file=buffer, force_terminal=True, color_system='truecolor'
        )
        live = out.LiveText('First message')
        time.sleep(0.5)
        assert 'First message' in out.ansi_clean(buffer.getvalue())
        live.info('Info message')
        time.sleep(0.5)
        assert 'Info message' in out.ansi_clean(buffer.getvalue())
        live.warn('Warn message')
        time.sleep(0.5)
        assert 'Warn message' in out.ansi_clean(buffer.getvalue())
        live.error('Error message', end=False)
        time.sleep(0.5)
        assert 'Error message' in out.ansi_clean(buffer.getvalue())
        live.success('Success message', end=False)
        time.sleep(0.5)
        assert 'Success message' in out.ansi_clean(buffer.getvalue())
    finally:
        out.CONSOLE = original_console
    assert live._running is True
    live.cancel()
    assert live._running is False


def test_live_concurrent():
    buffer = StringIO()
    original_console = out.CONSOLE
    try:
        out.CONSOLE = Console(
            file=buffer, force_terminal=True, color_system='truecolor'
        )
        live_1 = out.live('First message')
        live_2 = out.live('Second message')
        assert live_1 == live_2
    finally:
        out.CONSOLE = original_console


def test_live_text_threading():
    buffer = StringIO()
    original_console = out.CONSOLE
    try:
        out.CONSOLE = Console(
            file=buffer, force_terminal=True, color_system='truecolor'
        )

        live = out.LiveText('First message')
        assert live.is_alive is True
        live.stop()
        assert live.is_alive is False
        live.start()
        assert live.is_alive is True
        live.start()
        assert live.is_alive is True
        live.stop()
        assert live.is_alive is False

        live = out.LiveText('First message')
        live.error('Error message')
        assert 'Error message' in out.ansi_clean(buffer.getvalue())
        assert live.is_alive is False

        live = out.LiveText('First message')
        assert live.is_alive is True
        live.success('Success message')
        assert live.is_alive is False
        assert 'Success message' in out.ansi_clean(buffer.getvalue())

        live = out.LiveText('First message')
        live.warn('Warn message', end=True)
        assert live.is_alive is False
        assert 'Warn message' in out.ansi_clean(buffer.getvalue())

        live = out.LiveText('First message')
        live.info('Info message', end=True)
        assert live.is_alive is False
        assert 'Info message' in out.ansi_clean(buffer.getvalue())
    finally:
        out.CONSOLE = original_console


def test_table(capsys):
    data = [
        {'name': 'Luke', 'age': 18, 'is_student': True},
        {'name': 'Elizabeth', 'age': 101, 'is_student': False},
    ]
    buffer = StringIO()
    original_console = out.CONSOLE
    try:
        out.CONSOLE = Console(
            file=buffer, force_terminal=True, color_system='truecolor'
        )
        out.table(data, border=False, title='My title', style_cols='red')
        raw_output = buffer.getvalue()
        assert '\x1b[' in raw_output
        assert '\x1b[31m' in raw_output or '\x1b[91m' in raw_output
    finally:
        out.CONSOLE = original_console

    out.table(data, border=False, title='My title')
    printed = output(capsys)
    assert 'My title' in printed
    assert 'Is student' in printed
    assert '│' not in printed
    assert 'Elizabeth' in printed

    out.table(data, border=True, title='My title')
    printed = output(capsys)
    assert 'My title' in printed
    assert 'Is student' in printed
    assert '│' in printed
    assert '│ Elizabeth │' in printed

    out.table(data, border=True, padding=(0, 0))
    printed = output(capsys)
    assert '│Elizabeth│' in printed

    out.table([])
    printed = output(capsys)
    assert '' == printed


def test_var_dump(capsys):
    out.var_dump([1, 2, 3, 4])
    assert '[1, 2, 3, 4]' in output(capsys)

    out.var_dump(
        {
            'number': 1,
            'list': ['a', 'b', 'c'],
            'dict': {
                'key a': 'value a',
                'key b': 'value b',
            },
        }
    )
    printed = output(capsys)
    assert "'number': 1," in printed
    assert "'list': ['a', 'b', 'c']," in printed
    assert "'dict': {'key a': 'value a'," in printed


def test_ask(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'y')
    response = out.ask('You are sure?')
    assert response == 'y'
    printed = output(capsys)
    assert 'You are sure?' in printed
    assert '[y/n]' in printed

    monkeypatch.setattr('builtins.input', lambda: 'answer')
    response = out.ask('What is your name?', choices=None)
    assert response == 'answer'
    printed = output(capsys)
    assert 'What is your name?' in printed
    assert '[y/n]' not in printed

    monkeypatch.setattr('builtins.input', lambda: 'yes')
    response = out.ask('Continue?', choices=['yes', 'no'])
    assert response == 'yes'
    printed = output(capsys)
    assert 'Continue?' in printed
    assert '[yes/no]' in printed


def test_rule(capsys):
    out.rule('My rule')
    printed = output(capsys)
    assert 'My rule' in printed
    assert '─' in printed

    out.rule('My rule')
    printed = output(capsys)
    assert 'My rule' in printed
    assert '─' in printed

    live = out.live('Message in live')
    assert 'Message in live' in live._text
    out.rule('My rule')
    assert 'My rule' in live._text
    printed = output(capsys)
    assert 'My rule' in printed
    live.cancel()
    printed = output(capsys)
    assert 'My rule' not in printed


def test_no_ansi(capsys):
    out.setup(ansi=False)
    assert out.CONSOLE.no_color is True
    out.success('Success')
    assert '✓ Success' in output(capsys)
    out.warn('Warn')
    assert '▲ Warn' in output(capsys)
    out.error('Error')
    assert '✗ Error' in output(capsys)

    live = out.live('Message in live')
    assert 'Message in live' in live._text
    live.success('Success', end=False)
    time.sleep(1)
    assert '✓ Success' in live._text
    live.error('Error', end=False)
    assert '✗ Error' in live._text
    live.cancel()

    output(capsys)
    out.setup(ansi=True)
    assert out.CONSOLE.no_color is False
    out.success('Success')
    assert '✓' not in output(capsys)
    out.warn('Warn')
    assert '▲' not in output(capsys)
    out.error('Error')
    assert '✗' not in output(capsys)
    out.success('Success', icon=True)
    assert '✓ Success' in output(capsys)
    out.warn('Warn', icon=True)
    assert '▲ Warn' in output(capsys)
    out.error('Error', icon=True)
    assert '✗ Error' in output(capsys)
