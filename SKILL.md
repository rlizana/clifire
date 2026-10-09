---
name: clifire
description: Build Python command-line applications with the CliFire framework. Use when writing code that imports clifire, defines @command.fire functions or command.Command subclasses, uses cmd.app.shell, out messages, Config YAML or Jinja2 Template, or when the user mentions CliFire, the fire CLI, or asks to create a Python CLI with arguments, options, grouped commands, or rich console output.
---

# CliFire

Minimal Python CLI framework (`pip install clifire`). Runtime dependencies:
`jinja2`, `pyyaml`, `rich`. Python >= 3.8. Full docs:
<https://rlizana.github.io/clifire>.

## Application layout

Two entry styles:

**1. Declarative (recommended for simple CLIs).** Create `fire/` folder (or
`fire.py`) in the project root; the `fire` console script walks up from the cwd,
loads every `*.py` file there and runs the matching command:

```python
from clifire import command, out


@command.fire
def hello(cmd, user: str = "", _sudo: bool = False):
    """
    Display a greeting on the console.

    Args:
        user: Name of the user to greet. If empty, the system user is used.
        _sudo: Run the command with sudo privileges.
    """
    if not user:
        sudo = "sudo" if _sudo else ""
        user = cmd.app.shell(f"{sudo} whoami").stdout
    out.info(f"Hi {user}!")
```

Run: `fire hello Rob`.

**2. Programmatic.** Create the `App` first (decorators register themselves on
`App.current_app` at import time), then register classes, then fire:

```python
from clifire import application, command, out


class DeployCommand(command.Command):
    _name = "deploy"
    _help = "Deploy the application"

    target = command.Field(pos=1, help="Deployment target")
    force = command.Field(default=False, help="Force deployment")

    def fire(self):
        out.success(f"Deployed to {self.target}")


app = application.App(name="myapp", version="1.0.0")
app.add_command(DeployCommand)
app.fire()
```

`app.fire(command_line=None)` uses `sys.argv` when no line is given. Exit codes:
`App.fire` returns/propagates int codes; use `out.critical(msg, code)` to abort.

## Decorator rules (`@command.fire`)

- First parameter is `cmd` (the Command instance); skip it in the signature.
- Parameter **without** leading underscore = positional argument, in signature
  order. Parameter **with** `_` prefix = option (`_sudo` -> `--sudo`, auto-alias
  `s` = first letter).
- Parameter annotations/defaults define the type: `str` default -> `str`,
  `''`/`False`/`0` default -> optional, `None` default -> **required**, `list`
  -> consumes all remaining tokens (arguments) or splits on commas (options).
- Function name becomes the command name: uppercases and `_` become dots.
  `update_version` -> `fire update version`; `doc_build` -> `fire doc build`.
- The docstring is the help text: first line = summary, `Args:` section with
  `param: help` lines documents each parameter.

## Class commands (`command.Command` subclass)

- Class attrs `_name` (required, may contain dots for groups), `_help`.
- Each `command.Field(...)` is an argument (`pos=1, 2, ...`) or option
  (omit `pos`). Field kwargs: `pos`, `help`, `default`, `alias` (list, e.g.
  `['o', 'int']`), `force_type`.
- Lifecycle: `__init__` -> `init()` (override for setup) -> `launch()` ->
  `parse()` -> `fire()` (override, your entry point). Return an int from
  `fire()` to exit with that code.
- `self.app` (App), `self.context` (dict), `self.extra_args` (unconsumed
  tokens), `self.command_line`.

## Built-in commands

Automatically registered on every App (disable by passing
`command_help=None` / `command_version=None` / `command_completion=None` /
`command_skill=None` to `App(...)`):

- `fire help [command]` - auto-generated help from docstrings/Fields.
- `fire version` - app name + version.
- `fire completion [bash|zsh|fish]` - print shell completion script;
  `fire completion --install` writes it for the current shell.
- `fire skill [print|path|install]` - print, locate or install this AI agent
  skill file (`--target auto|all|project|claude|crush`).

Global options on every app: `-v/--verbose` (debug output + rich traceback),
`--no-ansi` (plain output), `-h/--help`.

## Output (`from clifire import out`)

- `out.info/success/warn/error` - styled messages; `out.critical(msg, code=1)`
  prints error and `sys.exit(code)`.
- `out.debug/debug2` - only visible with `-v`.
- `out.table(data, title=..., border=...)` - rich table from a list of dicts.
- `out.live('text')` / `out.LiveText` - spinner-style updating line.
- `out.ask(text, choices=['y', 'n'])` - prompt; `out.rule(text)` - section
  separator; `out.var_dump(obj)`; `out.ansi_clean(text)` - strip ANSI codes.

## Shell execution

`result = cmd.app.shell('ls -la', path='.', env={'K': 'V'}, capture_output=True, check=False)`
returns a `Result` with `.code`, `.stdout`, `.stderr`; `if result:` is True on
exit code 0. `cmd.app.path(*parts)` joins paths expanding `~`.

## Config (YAML)

```python
app = application.App(config_files=["~/.myapp.yml"], config_create=True)
app.config.query_get("db.host", default="localhost")
app.config.query_set("db.port", 5432)
```

First existing file wins; attributes are also plain object access
(`app.config.db.host` after `query_set`).

## Templates (Jinja2)

```python
app = application.App(template_folder="./templates")
app.template.render("file.jinja2", title="Hi")
app.template.write("file.jinja2", "out.txt", mark="# generated", title="Hi")
```

`os` is injected into the render context. With `mark=`, only the block between
the two identical mark lines is replaced.

## Errors and exit codes

- Raise `clifire.errors.CommandError('message', code=50)` inside a command;
  `App.fire` converts it to `out.critical` with that code.
- Built-in codes: 10 = no command provided, 20 = command not found,
  30 = `CommandException`, 40 = `FieldException` (bad option/argument value,
  missing required argument).
- `KeyboardInterrupt` prints an error and re-raises.

## Gotchas

- `@command.fire` needs an `App` to exist first (`App.current_app`); create the
  App before importing decorated modules, or use the `fire/` folder convention
  (the runner creates the App for you).
- `Field(default=None)` means **required**, not "None value".
- Option aliases are first letters by default: two commands in the same app
  with parameters starting with the same letter raise
  `Duplicate option alias`.
- Unknown flags do not error: they land in `cmd.extra_args`.
- `out.setup()` is called inside `App.fire`; printing before that uses default
  console settings.
- Verbose mode (`-v`) must be passed anywhere in the line; it is parsed before
  the command itself.
