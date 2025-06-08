# Decorators in CliFire

In CliFire, decorators simplify the creation and registration of commands in a clean and elegant way. With the `@command.fire` decorator, you can easily transform regular functions into CLI commands.

## What is a Decorator?

In Python, a decorator is a function that receives another function and extends or modifies it without altering its structure. In the context of CliFire, the decorator:

- **Registers the command** in the application.
- **Extracts information** (name, arguments, docstring) needed for the command.
- **Prepares the function** to be invoked from the command line.

## Using the `@command.fire` Decorator

The `@command.fire` decorator is the simplest way to convert a function into a command within CliFire. For example, create the file `fire/greet.py` with the following content:

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

By applying `@command.fire`:

- The `greet` function is transformed into a command object.
- Information such as the command name and its arguments is extracted from the docstring.
- The command is automatically registered to be used in the CLI.

## Advantages of Using Decorators

- **Simplicity:** Define commands in just a few lines of code.
- **Organization:** Separates command logic from CLI interface configuration.
- **Flexibility:** Allows you to define arguments and options using type annotations and docstring comments.

## Automatic Command Registration

When you define a function with `@command.fire`, the decorator performs the following operations:

1. Obtains the command name using `func.__name__` or a custom attribute.
2. Processes the docstring to extract the description and details for each argument.
3. Dynamically creates a class that inherits from `command.Command` representing the command.
4. Registers this command in the current application using `get_current_app().add_command(...)`.

## Command Execution

The help is automatically built from the docstring, enabling users to quickly understand how to use the command:

![Help](../../assets/records/help.svg)

You can execute the `greet` command directly:
![Greet](../../assets/records/greet.svg)

## The `fire` Command

The `fire` command is the main entry point for interacting with your CLI application. It allows you to execute commands and pass arguments and options.

`fire` searches for your commands either in a `fire.py` file or in the `fire/*.py` folder in the directory where it is launched.

## Customization

If you need to modify a command's behavior:
- You can adjust the options and arguments in the decorator.
- Use clear docstrings to define the command help.
- Explore the implementation of `@command.fire` in [`clifire/command.py`](clifire/command.py) to see how the information is processed.

With this decorator-based mechanism, CliFire allows you to build commands quickly while keeping your code clean and organized.

Start using decorators to simplify the creation of your commands and take advantage of the flexibility that CliFire offers!
