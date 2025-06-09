from clifire import command, out


@command.fire
def hello(cmd, user: str = "", _sudo: bool = False):
    """
    Display a greeting on the console

    Args:
        user: Name of the user to greet. If empty, it will use the current
            system user.
        _sudo: It will run the command with sudo privileges.
    """
    out.debug(f"Sudo = {_sudo}")
    if not user:
        sudo = "sudo" if _sudo else ""
        user = cmd.app.shell(f"{sudo} whoami").stdout
    out.info(f"Hi {user}!")


@command.fire
def nodoc(cmd):
    out.info("Command without doc")
