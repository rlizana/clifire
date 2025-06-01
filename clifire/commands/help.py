from .. import command, out


class CommandHelp(command.Command):
    _name = "help"
    _help = "Show this help or help for a command"

    command = command.Field(
        pos=1,
        help="Command to show help",
        default=["help"],
    )

    def print(self, txt):
        out._print(txt)

    def get_help(self, cmd):
        lines = (cmd._help or cmd.__doc__ or "").strip().splitlines()
        return lines[0]

    def print_description(self, cmd):
        title = "Description:"
        self.print(f"[bold]{title}[/bold]")
        self.print(f"  {self.get_help(cmd)}")
        self.print("")

    def print_usage(self, cmd):
        title = "Usage:"
        self.print(f"[bold]{title}[/bold]")
        args = [
            f"<{n}>" if cmd._fields[n].is_required else f"[<{n}>]"
            for n in cmd._argument_names
        ]
        cmd_name = cmd._name.replace(".", " ")
        self.print(f'  [cyan]{cmd_name}[/cyan] [[options]] {" ".join(args)}')
        self.print("")

    def print_arguments(self, cmd):
        data = []
        for name in cmd._argument_names:
            field = cmd._fields[name]
            data.append({"name": name, "help": field.help})
        if not data:
            return False
        title = "Arguments:"
        self.print(f"[bold]{title}[/bold]")
        out.table(
            data, border=False, show_header=False, style_cols={"name": "cyan"}
        )
        self.print("")

    def print_options(self, cmd):
        options = {}
        for name in cmd._options:
            field = cmd._options[name]
            if isinstance(field, str):
                field = cmd._fields[field]
            name = f"-{name}" if len(name) == 1 else f"--{name}"
            options.setdefault(field, []).append(name)
        if not options:
            return False
        data = []
        for field, names in options.items():
            short = ", ".join(sorted([n for n in names if len(n) == 2]))
            name = ", ".join(sorted([n for n in names if len(n) != 2]))
            data.append({"short": short, "name": name, "help": field.help})
        title = "Options:"
        self.print(f"[bold]{title}[/bold]")
        out.table(
            sorted(data, key=lambda d: d["short"]),
            border=False,
            show_header=False,
            style_cols={"short": "cyan", "name": "cyan"},
        )
        self.print("")

    def print_options_global(self):
        options = {}
        for name in self.app.options:
            field, _value = self.app.options[name]
            if isinstance(field, str):
                field, _value = self.app.options[field]
            name = f"-{name}" if len(name) == 1 else f"--{name}"
            options.setdefault(field, []).append(name)
        if not options:
            return False
        data = []
        for field, names in options.items():
            short = ", ".join(sorted([n for n in names if len(n) == 2]))
            name = ", ".join(sorted([n for n in names if len(n) != 2]))
            data.append({"short": short, "name": name, "help": field.help})
        title = "Global options:"
        self.print(f"[bold]{title}[/bold]")
        out.table(
            sorted(data, key=lambda d: d["short"]),
            border=False,
            show_header=False,
            style_cols={"short": "cyan", "name": "cyan"},
        )
        self.print("")

    def print_commands(self):
        data = [
            {"name": cls._name, "help": self.get_help(cls)}
            for cls in self.app.commands.values()
            if "." not in cls._name
        ]
        title = "Available Commands:"
        self.print(f"[bold]{title}[/bold]")
        out.table(
            data, border=False, show_header=False, style_cols={"name": "cyan"}
        )
        self.print("")

    def run(self):
        cmd = self.app.get_command(" ".join(self.command))
        self.print_description(cmd)
        self.print_usage(cmd)
        self.print_arguments(cmd)
        self.print_options(cmd)
        self.print_options_global()
        if cmd._name == "help":
            self.print_commands()
