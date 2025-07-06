import atexit
import re
import sys
import threading
import time
from typing import Any

from rich import traceback
from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table

traceback.install(
    show_locals=True,
    theme='monokai',
    suppress=[],
    max_frames=2,
)

CONSOLE = Console()
CONSOLE_WIDTH = CONSOLE.width

COLOR_NORMAL = 'white'
COLOR_DEBUG = 'grey50'
COLOR_DEBUG2 = 'bright_black'
COLOR_INFO = 'blue'
COLOR_SUCCESS = 'green'
COLOR_WARN = 'yellow'
COLOR_ERROR = 'red'


def setup(ansi: bool = True):
    if ansi:
        CONSOLE.no_color = False
        CONSOLE.highlight = True
        CONSOLE.soft_wrap = True
        CONSOLE.width = CONSOLE_WIDTH
        debug('Console output setup with ANSI')
    else:
        CONSOLE.no_color = True
        CONSOLE.highlight = False
        CONSOLE.soft_wrap = False
        CONSOLE.width = 10000
        debug('Console output setup with no ANSI')


class LiveText:
    def __init__(self, text: str = '', refresh_per_second: int = 10):
        self._live = None
        self._running = False
        self._thread = None
        self._text = ''
        atexit.register(self.cancel)
        self.elapsed_time = 0
        self.refresh_per_second = refresh_per_second
        self.info(text)
        self.start()

    @property
    def is_alive(self):
        return self._running

    def _start(self):
        with Live(
            console=CONSOLE,
            refresh_per_second=self.refresh_per_second,
        ) as live:
            self._live = live
            self._live.update(self._text)
            start_time = time.time()
            while self._running:
                self.elapsed_time = time.time() - start_time
                display_message = (
                    f'[grey0]({self.elapsed_time: .1f}s)[/grey0] '
                    f'{self._text}\n'
                )
                self._live.update(display_message)
                time.sleep(1 / self.refresh_per_second)
            self._live.update(self._text)

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._running = True
        self._thread = threading.Thread(target=self._start, daemon=True)
        self._thread.start()

    def cancel(self):
        self._text = ''
        self.stop()

    def stop(self):
        self._running = False
        if self._text != '':
            CONSOLE.print(self._text)
        if self._thread and self._thread.is_alive():
            self._live.transient = True
            self._text = text_color('')
            self._thread.join(timeout=1.0)
            self._live.update(self._text)

    def info(self, text: str, end=False):
        self._text = text_color(text, color=COLOR_INFO)
        if end:
            self.stop()

    def warn(self, text: str, end=False):
        self._text = text_color(text, color=COLOR_WARN)
        if end:
            self.stop()

    def success(self, text: str, end=True):
        self._text = text_color(text, color=COLOR_SUCCESS)
        if end:
            self.stop()

    def error(self, text: str, end=True):
        self._text = text_color(text, color=COLOR_ERROR)
        if end:
            self.stop()


_current_live = None


def live(text: str = '', refresh_per_second: int = 10):
    global _current_live
    if _current_live:
        return _current_live
    _current_live = LiveText(text, refresh_per_second=refresh_per_second)
    return _current_live


def table(
    data: list[dict[str, Any]],
    title: str = '',
    border: bool = True,
    show_header: bool = True,
    style_cols: dict[str, str] = None,
    padding: tuple = None,
    style: str = None,
):
    if not data:
        return
    keys = list(data[0].keys())
    tbl = Table(title=title, show_header=show_header, style=style)
    if not border:
        tbl.box = None
        tbl.padding = (0, 2)
    if padding is not None:
        tbl.padding = padding
    for key in keys:
        justify = 'right' if isinstance(data[0][key], (int, float)) else 'left'
        _style_col = None
        if isinstance(style_cols, dict):
            _style_col = style_cols.get(key, None)
        elif isinstance(style_cols, str):
            _style_col = style_cols
        tbl.add_column(
            key.replace('_', ' ').capitalize(),
            justify=justify,
            style=_style_col,
        )
    for row in data:
        tbl.add_row(*(str(row.get(key, '')) for key in keys))
    CONSOLE.print(tbl)


def ansi_clean(text: str) -> str:
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)


def text_color(text: str, color: str = COLOR_NORMAL) -> str:
    return f'[{color}]{text}[/{color}]'


def _print(text: str, color: str = COLOR_NORMAL) -> None:
    CONSOLE.print(text_color(text, color=color))


def info(text: str) -> None:
    _print(text, COLOR_INFO)


def success(text: str) -> None:
    _print(text, COLOR_SUCCESS)


def warn(text: str) -> None:
    _print(text, COLOR_WARN)


def error(text: str) -> None:
    _print(text, COLOR_ERROR)


def critical(text: str, code: int = 1) -> None:
    error(text)
    sys.exit(code)


def _debug(text: str, color: str) -> None:
    from clifire import application

    app = application.App.current_app
    if not app or app.get_option('verbose'):
        _print(text, color)


def debug(text: str) -> None:
    _debug(text, COLOR_DEBUG)


def debug2(text: str) -> None:
    _debug(f'· {text}', COLOR_DEBUG2)


def var_dump(var) -> None:
    CONSOLE.print(var, highlight=True)


def ask(text: str, choices: list[str] = ['y', 'n']):  # noqa: B006
    return Prompt.ask(
        text, choices=choices, default=choices[0] if choices else None
    )
