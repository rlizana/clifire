# ![CliFire Logo](docs/docs/assets/logo-for-readme.svg) CliFire

[![CI Status](https://github.com/rlizana/clifire/actions/workflows/actions.yml/badge.svg)](https://github.com/rlizana/clifire/actions/workflows/actions.yml)
[![Coverage Status](https://coveralls.io/repos/github/rlizana/clifire/badge.svg?branch=main)](https://coveralls.io/github/rlizana/clifire?branch=main)
[![PyPI version](https://badge.fury.io/py/clifire.svg)](https://badge.fury.io/py/clifire)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Minimal CLI framework to build Python commands quickly and elegantly.**

CliFire is a lightweight Python library designed to simplify the creation of command-line interfaces (CLI). It allows developers to define commands, options, and arguments in a straightforward way, making it easy to build complex CLI applications without the overhead of bigger frameworks.

## Key Features

- **Two Usage Styles:** Define commands using decorators or classes.
- **Intuitive Syntax:** Focus on writing application logic without worrying about CLI infrastructure.
- **Arguments & Options:** Flexible parsing with positional arguments and command options.
- **Grouped Commands:** Organize related commands using a dot-based naming convention.
- **Formatted Output:** Leverage the [Rich library](https://rich.readthedocs.io/) for colorful and styled messages.
- **Templates:** Generate files using [Jinja2](https://jinja.palletsprojects.com/) templates.
- **Centralized Configuration:** Manage configuration via YAML using the `Config` module.

## Installation

Install CliFire using pip:

```bash
pip install clifire
```

Or with Poetry:

```bash
poetry add clifire
```

Or with uv:

```bash
uv add clifire
```

Or with rye:

```bash
rye add clifire
```

## Quick Start

Create a simple CLI command using decorators. For example, save the following as `fire/hello.py`:

```python
from clifire import command, out

@command.fire
def hello(cmd, user: str = "", _sudo: bool = False):
    """
    Display a greeting on the console.

    Args:
        user: Name of the user to greet. If empty, the current system user is used.
        _sudo: Run the command with sudo privileges.
    """
    if not user:
        sudo = 'sudo' if _sudo else ''
        user = cmd.app.shell(f"{sudo} whoami").stdout
    out.info(f'Hi {user}!')
```

Then run:

```bash
fire hello Rob
```

In action:
![Demo](./docs/docs/assets/records/quick_start_hello.svg)


For more details, see our [Quick Start Guide](https://rlizana.github.io/clifire/en/quick-start).

## Documentation

The full documentation is available on GitHub Pages in [English](https://rlizana.github.io/clifire/en) and [Spanish](https://rlizana.github.io/clifire/es/es). It covers topics such as:

- [CliFire Basics](https://rlizana.github.io/clifire/en/user-guide/basics)
- [Decorators](https://rlizana.github.io/clifire/en/user-guide/decorators)
- [Class-based Commands](https://rlizana.github.io/clifire/en/user-guide/classes)
- [Options and Arguments](https://rlizana.github.io/clifire/en/user-guide/options-arguments)
- [Grouped Commands](https://rlizana.github.io/clifire/en/user-guide/grouped-commands)
- [Output and Styling](https://rlizana.github.io/clifire/en/user-guide/output)
- [Configuration](https://rlizana.github.io/clifire/en/user-guide/config)
- [Templates](https://rlizana.github.io/clifire/en/user-guide/templates)
- [Changelog](https://rlizana.github.io/clifire/en/changelog)
- [Contributing](https://rlizana.github.io/clifire/en/contributing)

## For AI agents

This project ships an [Agent Skill](https://agentskills.io) so coding agents can
learn the framework without reading the whole source. The file lives at
[`SKILL.md`](./SKILL.md) and is also bundled inside the PyPI package:

```bash
fire skill           # print the skill file content
fire skill path      # print the skill file location
fire skill install   # copy it where your agent will find it (Claude Code, Crush, ...)
```

`fire skill install` detects the agent hosts present in your home directory and
the current project (`.claude/skills/`, `.agents/skills/`,
`~/.config/crush/skills/`, `~/.claude/skills/`); use `--target all` to force all
of them. The package is typed (`py.typed`), so LSPs and IDEs also get completions.

## Development

CliFire is an open-source project, and contributions are welcome! If you find a bug, have a feature request, or want to contribute improvements, please open an issue or submit a pull request.

> For development, we use [uv](https://docs.astral.sh/uv/), a fast Python environment and dependency manager. If you don't have it installed, run:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

To contribute to CliFire:

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/<your-username>/clifire.git
   cd clifire
   ```
3. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/my-feature
   ```
4. **Install development dependencies**:

   ```bash
   uv sync
   ```
5. **Run tests** to ensure everything works:
   ```bash
   uv run pytest
   # or to check coverage:
   uv run coverage run -m pytest && uv run coverage html
   ```

   You can also use the `fire coverage` command to run the tests and generate the coverage report:
   ```bash
   uv run fire coverage
   ```
6. **Update the CHANGELOG.md** with your changes.
7. **Commit and push** your changes, and then create a pull request.

For further contribution details, please see our [Contributing Guide](https://rlizana.github.io/clifire/en/contributing).

## License

CliFire is released under the MIT License. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.
