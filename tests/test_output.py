import time
from io import StringIO

import pytest
from rich.console import Console

from clifire import application, out


@pytest.fixture(autouse=True)
def reset_current_app():
    application.App.current_app = None
    yield


def output(capsys):
    captured = capsys.readouterr()
    return out.ansi_clean(captured.out)


def test_info(capsys):
    out.info("Info sample message")
    assert "Info sample message\n" == output(capsys)


def test_success(capsys):
    out.success("Success sample message")
    assert "Success sample message\n" == output(capsys)


def test_warn(capsys):
    out.warn("Warn sample message")
    assert "Warn sample message\n" == output(capsys)


def test_error(capsys):
    out.warn("Error sample message")
    assert "Error sample message\n" == output(capsys)


def test_critical(capsys):
    with pytest.raises(SystemExit) as excinfo:
        out.critical("Critical sample message 1")
    assert "1" == str(excinfo.value)
    assert "Critical sample message 1\n" == output(capsys)
    with pytest.raises(SystemExit) as excinfo:
        out.critical("Critical sample message", 99)
    assert "99" == str(excinfo.value)
    assert "Critical sample message\n" == output(capsys)


def test_debug(capsys):
    out.debug("Debug sample message")
    assert "Debug sample message\n" == output(capsys)


def test_live_text():
    buffer = StringIO()
    original_console = out.CONSOLE
    out.CONSOLE = Console(
        file=buffer, force_terminal=True, color_system="truecolor"
    )
    live = out.LiveText("First message")
    time.sleep(0.5)
    assert "First message" in out.ansi_clean(buffer.getvalue())
    live.info("Info message")
    time.sleep(0.5)
    assert "Info message" in out.ansi_clean(buffer.getvalue())
    live.warn("Warn message")
    time.sleep(0.5)
    assert "Warn message" in out.ansi_clean(buffer.getvalue())
    live.error("Error message", end=False)
    time.sleep(0.5)
    assert "Error message" in out.ansi_clean(buffer.getvalue())
    live.success("Success message", end=False)
    time.sleep(0.5)
    assert "Success message" in out.ansi_clean(buffer.getvalue())
    out.CONSOLE = original_console
    assert live._running is True
    live.cancel()
    assert live._running is False


def test_live_text_threading():
    buffer = StringIO()
    original_console = out.CONSOLE
    out.CONSOLE = Console(
        file=buffer, force_terminal=True, color_system="truecolor"
    )

    live = out.LiveText("First message")
    assert live.is_alive is True
    live.stop()
    assert live.is_alive is False
    live.start()
    assert live.is_alive is True
    live.start()
    assert live.is_alive is True
    live.stop()
    assert live.is_alive is False

    live = out.LiveText("First message")
    live.error("Error message")
    assert "Error message" in out.ansi_clean(buffer.getvalue())
    assert live.is_alive is False

    live = out.LiveText("First message")
    assert live.is_alive is True
    live.success("Success message")
    assert live.is_alive is False
    assert "Success message" in out.ansi_clean(buffer.getvalue())

    live = out.LiveText("First message")
    live.warn("Warn message", end=True)
    assert live.is_alive is False
    assert "Warn message" in out.ansi_clean(buffer.getvalue())

    live = out.LiveText("First message")
    live.info("Info message", end=True)
    assert live.is_alive is False
    assert "Info message" in out.ansi_clean(buffer.getvalue())

    out.CONSOLE = original_console


def test_table(capsys):
    data = [
        {"name": "Luke", "age": 18, "is_student": True},
        {"name": "Elizabeth", "age": 101, "is_student": False},
    ]
    out.table(data, border=False, title="My title")
    printed = output(capsys)
    assert "My title" in printed
    assert "Is student" in printed
    assert "│" not in printed
    assert "Elizabeth" in printed

    out.table(data, border=True, title="My title")
    printed = output(capsys)
    assert "My title" in printed
    assert "Is student" in printed
    assert "│" in printed
    assert "│ Elizabeth │" in printed

    out.table(data, border=True, padding=(0, 0))
    printed = output(capsys)
    assert "│Elizabeth│" in printed

    out.table([])
    printed = output(capsys)
    assert "" == printed


def test_var_dump(capsys):
    out.var_dump([1, 2, 3, 4])
    assert "[1, 2, 3, 4]" in output(capsys)

    out.var_dump(
        {
            "number": 1,
            "list": ["a", "b", "c"],
            "dict": {
                "key a": "value a",
                "key b": "value b",
            },
        }
    )
    printed = output(capsys)
    assert "\n    'number': 1," in printed
    assert "\n    'list': ['a', 'b', 'c']," in printed
    assert "\n    'dict': {'key a': 'value a'," in printed
