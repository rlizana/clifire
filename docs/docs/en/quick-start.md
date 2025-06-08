# Quick Start Guide - Getting Started with CliFire

Welcome to the Quick Start Guide for CliFire, a minimalist framework for creating command line interfaces in Python quickly and elegantly.

## Installation

You can install CliFire from PyPI or directly using Poetry:

### From PyPI

```bash
pip install clifire
```

### Using Poetry

```bash
poetry add clifire
```

## Basic Usage

CliFire allows you to define commands using decorators or classes. Here’s an example using a decorator to greet the user:

```python
from clifire import command, out


@command.fire
def greet(cmd, name: str = "World", _end_char: str = "?"):
    """
    Greets the user.

    Args:
        name: Name of the user to greet. Defaults to "World".
        _end_char: Character to use at the end of the greeting. Defaults to "?".
    """
    result = cmd.app.shell("whoami")
    out.info(f"System user: {result.stdout}")
    out.success(f"Hello {name}{_end_char}")
```

### Running the Command

Save the file as `fire.py` or create a `fire` directory and place the file inside with a `.py` extension.

Help is automatically built from the docstring, allowing users to quickly understand how to use the command:

![Help](../assets/records/help.svg)

You can run the `greet` command directly:
![Greet](../assets/records/greet.svg)

## Main Features

- **Simple Command Definition:** Use decorators or classes to create dynamic commands.
- **Handling of Arguments and Options:** Define arguments and options to customize the behavior of your commands.
- **Formatted Output:** Uses the `out` module to display messages with styles and colors by leveraging the Rich library.
- **Centralized Configuration:** Manage your application's configuration through the `Config` class.
- **File Templates:** Create files using Jinja2 templates via the `Template` class.

## Next Steps

- For more details on the API and configuration, consult the [User Documentation](user-guide/basics.md).
- Check the [API Reference](api/index.md) to see all available functions and classes.
- Look at practical examples in the [Examples](examples.md) section.

Start creating your commands and enjoy a minimalist and powerful experience with CliFire!
