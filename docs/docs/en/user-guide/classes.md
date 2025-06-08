# Class-based Commands

In addition to using decorators, CliFire allows you to define commands using classes. This approach is useful when you need more customization or complex logic in your commands.

## Defining a Command with Classes

To create a class-based command, inherit from `command.Command` and set the following properties:

- **`_name`**: The name of the command. If you want to group commands, use dots (for example, `db.create`).
- **`_help`**: A brief description that will be displayed in the help.
- **Fields/Arguments**: Define arguments and options as class attributes using `command.Field`.

Basic example:

```python
from clifire import command, out

class CommandGreet(command.Command):
    _name = "greet"
    _help = "Greets the user in a personalized way"

    # Define a field for the name (non-option argument)
    name = command.Field(
        pos=1,
        help="User's name",
        default="World",
        alias=[],
    )

    # Define a field to enable informal greeting (option)
    informal = command.Field(
        pos=None,
        help="Use informal greeting",
        default=False,
        alias=["-i"],
    )

    def fire(self):
        if self.informal:
            out.info(f"Hello, {self.name}! How's it going?")
        else:
            out.info(f"Good morning, {self.name}!")
```

## Registration and Execution

When the application is instantiated, the command is registered and can be executed from the command line:

```bash
$ fire greet
Good morning, World!

$ fire greet Alice -i
Hello, Alice! How's it going?
```

## Advantages of the Class-based Approach

- **Greater control and customization:** You can define your own methods and attributes to handle complex use cases.
- **Inheritance:** You can create base commands and extend them to share common behaviors.
- **Organization:** Results in a clear and modular structure when you have a large number of commands.

## Internal Details

When the application is instantiated, the commands defined as classes are registered. The application calls the `fire()` method of the corresponding command after parsing its arguments and options. Additionally:

- Fields are automatically updated based on the command parsing.
- Aliases and type conversions are managed in the `Field` class (see [command.py](../../clifire/command.py)).

With this mechanism, you can take full advantage of Python's flexibility and create commands with advanced behaviors without complicating the function-level syntax.

Explore and experiment by creating your own custom commands!
