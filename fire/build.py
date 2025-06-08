from clifire import command, out


@command.fire
def build(cmd):
    """
    Build the package and documentation
    """
    live = out.LiveText("Building ...")
    res = cmd.app.shell("poetry build")
    if res:
        live.success("Build success")
    else:
        live.error("Error on building packages.")
        out.error(res.stderr)
        return 1

    live.info("Building the docs ..")
    cmd.app.fire("doc build")


@command.fire
def coverage(cmd):
    """
    Launch tests with coverage
    """
    bash = "poetry run coverage run -m pytest && poetry run coverage html"
    cmd.app.shell(bash, capture_output=False)
