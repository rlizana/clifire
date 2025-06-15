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
        sudo = "sudo" if _sudo else ""
        user = cmd.app.shell(f"{sudo} whoami").stdout
    out.info(f"Hi {user}!")
