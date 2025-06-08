# Grouped Commands in CliFire

CliFire allows you to organize commands into groups using a dot-based naming convention. This is especially useful when your CLI application has many features, as it improves readability and organization.

## How It Works

To group commands, simply define the command name using a dot (`.`) to separate the group name from the specific command. For example, to group database-related commands, you can use names like `db.create` and `db.drop`.

When the command is registered, CliFire's help functionality (for example, in the help command) detects the `.` character and automatically groups the commands under the same category.

## Example of Defining Grouped Commands
The group is determined by the `_name` variable of the `Command` class or the method name when using decorators.

Here is an example of how to define grouped commands using classes:
```python
from clifire import command, out

class DbCreateCommand(command.Command):
    _name = "db.create"
    _help = "Create the database"

    def run(self):
        out.info("Database created.")

class DbDropCommand(command.Command):
    _name = "db.drop"
    _help = "Drop a database"

    def run(self):
        out.info("Database removed.")
```

## Registration and Execution

Register the commands in your application:

```python
from clifire import application

app = application.App(name="MyApp CLI", version="1.0")
app.add_command(DbCreateCommand)
app.add_command(DbDropCommand)
```

Then, when running the help command:

```bash
$ fire help
```

The output will display the grouped commands, for example:

```
Available Commands:

  db
    create          Create the database
    drop            Drop the database
```

## Using Grouped Commands with Decorators
You can use the same grouping convention with decorators to group commands. In this case, the groups are obtained from the method name by using the `_` character:

```python
from clifire import command, out

@command.fire
def db_create(cmd):
    """
    Create the database
    """
    out.info("Database created.")

@command.fire
def db_drop(cmd):
    """
    Drop the database.
    """
    out.info("Database removed.")
```

## Additional Tips

- **Name Consistency:** Make sure to follow a consistent naming convention for your commands (e.g., `group.command`) so that the grouping is intuitive.
- **Subgroups:** If needed, you can define multiple levels of grouping by using more than one dot (e.g., `db.table.create`).
- **Help Customization:** You can extend the help command functionality to modify how groups are displayed if necessary.

With this structure, you can organize your commands clearly and provide a better user experience for your CLI application.
