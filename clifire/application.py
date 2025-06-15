import os
import shlex
import subprocess
import sys

from clifire import command, commands, config, out, result, template


class App:
    current_app = None

    def __init__(
        self,
        name: str = "",
        version: str = "0.0.1 alpha",
        context: dict = None,
        option_verbose: bool = True,
        config_files: list = None,
        config_create: bool = False,
        command_help=commands.help.CommandHelp,
        command_version=commands.version.CommandVersion,
        template_folder=None,
    ):
        App.current_app = self
        self.name = name
        self.version = version
        self.options = {}
        if option_verbose:
            self._add_option_verbose()
        if context is None:
            context = {}
        self.context = context
        if config_files is None:
            config_files = []
        self.config = config.Config.get_config(
            config_files, create=config_create, **context
        )
        self.commands = {}
        if command_help:
            self.add_command(command_help)
        if command_version:
            self.add_command(command_version)
        self.template = None
        if template_folder:
            self.template = template.Template(template_folder)

    def _add_option_verbose(self):
        self.add_option(
            "verbose",
            command.Field(
                help="Verbose mode",
                default=False,
                alias="v",
            ),
        )
        command_line = sys.argv[1:]
        if "-v" in command_line or "--verbose" in command_line:
            self.set_option("verbose", True)

    def add_option(self, name: str, field: command.Field):
        self.options[name] = [field, field.default]
        for alias in field.alias:
            if alias.startswith("-"):
                alias = alias[2:] if alias.startswith("--") else alias[1:]
            alias = alias.replace("-", "_")
            if alias in self.options:
                raise command.CommandException(
                    f'Duplicate global option alias "{alias}"'
                )
            self.options[alias] = [name, None]

    def set_option(self, name: str, value):
        if name not in self.options:
            return False
        self.options[name][1] = value
        return True

    def get_option(self, name: str, default=None):
        if name not in self.options:
            return default
        return self.options[name][1]

    def add_command(self, cls: command.Command):
        if not cls._name:
            raise command.CommandException(
                f"The command {cls} has no name, please set _name var in class"
            )
        self.commands[cls._name] = cls

    def find_command(self, command_line: str):
        empty = False
        args = [p for p in shlex.split(command_line) if not p.startswith("-")]
        if not args:
            args = ["help"]
            empty = True
        while args:
            command_name = ".".join(args)
            if command_name in self.commands:
                return self.commands[command_name]
            args.pop()
        if empty:
            out.critical("No command provided.", code=10)
        return None

    def get_command(self, command_line: str) -> command.Command:
        cls = self.find_command(command_line)
        if cls:
            return cls(self, command_line)
        args = [p for p in shlex.split(command_line) if not p.startswith("-")]
        while args:
            group = ".".join(args + [""])
            commands = [k for k in self.commands.keys() if k.startswith(group)]
            if commands:
                cls = self.find_command("help")
                if cls:
                    return cls(self, command_line)
            last_arg = args.pop()
        out.critical(f'Command "{last_arg}" not found.', code=20)

    def fire(self, command_line: str = None):
        try:
            if command_line is None:
                out.debug(f"Sys argv value: {sys.argv}")
                command_line = " ".join(
                    shlex.quote(arg) for arg in sys.argv[1:]
                )
            cmd = self.get_command(command_line)
            res = cmd.launch(command_line)
            if type(res) is int and res != 0:
                sys.exit(res)
        except command.CommandException as e:
            out.critical(e, code=30)
        except command.FieldException as e:
            out.critical(e, code=40)

    @classmethod
    def shell(
        cls,
        cmd: str,
        capture_output: bool = True,
        env: dict = None,
        path: str = None,
        shell: bool = True,
        check: bool = False,
    ) -> result.Result:
        if path:
            os.chdir(path)
        env_vars = os.environ.copy()
        if env:
            env_vars.update(env)
        try:
            out.debug(f"Shell: {cmd}")
            proc = subprocess.run(
                cmd if shell else shlex.split(cmd),
                shell=shell,
                capture_output=capture_output,
                env=env_vars,
                check=check,
            )
            return result.Result(proc.returncode, proc.stdout, proc.stderr)
        except subprocess.CalledProcessError as e:
            return result.ResultError(e.stderr, e.returncode)

    @classmethod
    def path(cls, *args: list[str]) -> str:
        if len(args) == 0:
            args = (os.getcwd(),)
        exapnd_path = os.path.join(
            *(a.replace("~", os.path.expanduser("~")) for a in args)
        )
        return os.path.abspath(exapnd_path)
