from .. import command, out


class CommandVersion(command.Command):
    _name = "version"
    _help = "Display project version"

    def fire(self):
        out.info(f"{self.app.name} {self.app.version}")
