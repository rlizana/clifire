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
