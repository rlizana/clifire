# CliFire Basics

CliFire is a minimalist framework for creating command line applications in Python in a simple and elegant way. This guide introduces you to the fundamental concepts so you can start using it quickly.

We offer two approaches to use CliFire, via decorators or via classes:

- **Decorators:** They allow you to define commands quickly and easily without losing power or flexibility.
- **Classes:** They offer more detailed control over a command’s behavior, ideal for more complex applications.

The idea behind CliFire is to enable you to create CLI (Command Line Interface) applications quickly and easily by leveraging Python's features.

## 1. Commands

Commands are the essence of your CLI application. You can define them in two ways:

- **Using decorators:**
  Command creation is simplified with the `@command.fire` decorator.

  ```python
  from clifire import command, out

  @command.fire
  def hello(cmd, name: str = "World"):
      """
      Greets the user.

      Args:
          name: Name of the user. Defaults to "World".
      """
      out.info(f"Hello, {name}!")
  ```

- **Using classes:**
  Create a class that inherits from `command.Command` for more control over the command's behavior.

  ```python
  from clifire import command, out

  class CommandTest(command.Command):
      _name = "test"
      _help = "Test command"

      def fire(self):
          out.info("Executing test command")
  ```

## 2. Arguments and Options

CliFire allows you to define:

- **Global Options:** Settings that affect the entire application (for example, verbose mode).
- **Local Options:** Specific arguments and options for each command.

These options can be set using the `Field` class from the `command` module.

```python
from clifire import command

class CommandTest(command.Command):
    _name = "test"
    _help = "Test command"

    bool_option = command.Field(
        pos=1,
        help="Example boolean option",
        default=False,
        alias=["-v"],
    )

    def fire(self):
        if self.bool_option:
            print("Verbose option enabled")
        else:
            print("Verbose option disabled")
```

## 3. Configuration

The `Config` class manages your application's configuration. It allows you to read data from YAML files and write it, excluding private fields (those that begin with `_`).

```python
from clifire import config

conf = config.Config(config_file="config.yaml")
conf.name = "MyApp"
conf.version = "1.0.0"
conf.write()
```

*Note:* Private fields (e.g., `_secret`) are not saved in the configuration file.

## 4. Output and Styling

The `out` module uses the Rich library to display messages with different styles and colors:

- `out.info()`: Information.
- `out.success()`: Success.
- `out.warn()`: Warning.
- `out.error()`: Error.

```python
from clifire import out

out.info("This is an informational message")
```

## 5. Templates

The `Template` class allows you to generate files from Jinja2 templates. This is useful for creating files with dynamic content in an easy way.

```python
from clifire import template

tpl = template.Template(template_folder="templates")
content = tpl.render(
    "sample.jinja2",
    title="My Title",
    user="admin",
    items=["data1", "data2"]
)
```

Moreover, the `write` function of the template lets you save the rendered content to a file, with the option to insert or replace content delimited by markers.

This is useful for generating configuration files or custom scripts that can be easily updated in the future without affecting the rest of the file.

## 6. Execution Flow

1. **Command Definition:**
   Commands are defined using decorators or classes.

2. **Command Registration:**
   When the `App` is instantiated, commands are registered. By default, a help command is added that shows information about all available commands.

3. **Parsing and Execution:**
   When the application is run, the command line is parsed, the command to execute is identified, and its options and arguments are processed.

## Conclusion

With these basic concepts, you are ready to start using CliFire in your projects. The simplicity and flexibility of this framework will allow you to build powerful and customized CLI applications without complications.

For more details and advanced examples, consult the [User Documentation](../user-guide/index.md) and the [API Reference](../api/index.md).
