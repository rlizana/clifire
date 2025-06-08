# Options and Arguments in CliFire

In CliFire, commands can receive data both as **positional arguments** and **options**. These are defined using the `Field` class in the `command` module.

## Field Definition

Each field declared as an attribute in a command is recognized as:

- **Positional Argument:**
  If the field has a defined `pos` value (for example, `pos=1`), it is treated as an argument that is expected in a certain order.
  The arguments are assigned based on their position in the command line.

- **Option:**
  If `pos` is `False` or `None`, the field is interpreted as an option.
  Options are indicated on the command line with a single or double dash (for example, `-v` or `--verbose`).
  Additionally, aliases can be defined to facilitate its usage.

## Example of Field Definition in a Command

```python
from clifire import command, out

class CommandTest(command.Command):
    _name = "test"
    _help = "Example command using options and arguments"

    # Positional argument (for example, the first argument after the command name)
    filename = command.Field(
        pos=1,
        help="Name of the file to process",
        default="default.txt",  # default value if not specified
    )

    # Option activated with a flag (for example, -v for verbose)
    verbose = command.Field(
        pos=False,
        help="Detailed mode",
        default=False,
        alias=["v"],
    )

    # Option expecting a value (for example, --level=3)
    level = command.Field(
        pos=False,
        help="Level of detail",
        default=1,
        alias=["l"],
        force_type=int,
    )

    def run(self):
        out.info(f"File: {self.filename}")
        out.info(f"Verbose: {self.verbose}")
        out.info(f"Level: {self.level}")
```

In this example:
- **`filename`** is a positional argument: the first value not associated with an option is assigned.
- **`verbose`** is a boolean option: it is activated with `-v` or `--verbose`.
- **`level`** is an option expecting a numerical value; it can be used as `--level=3` or `-l 3`.

## Parsing and Conversion Process

When a command is executed:
1. **Parsing:**
   CliFire reads the command line and separates the **arguments** and **options** using `shlex.split()`.
   Positional arguments are assigned according to the order defined in the command’s `_argument_names` property.

2. **Value Conversion:**
   Each field uses its `convert` method to transform the received string into its expected type.
   For example:
   - If the field `level` is defined with `force_type=int`, the string will be converted to an integer.
   - If the field is of type `list`, comma separation can be used to obtain a list of elements.

3. **Validations:**
   - If a field is mandatory (without a default value), it is checked that a value has been provided.
   - Options can have aliases; these are normalized (for example, by removing dashes and replacing `-` with `_`) to avoid duplicates.

## Running a Command with Options and Arguments

When executing the above command from the terminal, you might experience different behaviors:

```bash
$ fire test myfile.txt -v --level=5
```

- The value `"myfile.txt"` will be assigned to `filename`.
- The `-v` option sets `verbose` to `True`.
- The argument `--level=5` will be converted to an integer (`5`) and assigned to `level`.

If some values are not provided, the default values defined will be used.

## Conclusion

Thanks to this flexible structure, CliFire makes it easy to define how data is received and processed in your commands. You can combine positional arguments and options with aliases, validations, and automatic type conversion, which simplifies the construction of robust and easy-to-use command line interfaces.

Experiment by creating your own commands and adjusting the options according to your application’s needs!
