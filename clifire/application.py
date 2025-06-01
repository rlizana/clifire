import os
import shlex
import subprocess
import sys

from . import command, commands, out, result


class App:
    def __init__(
        self,
        name: str = "",
        version: str = "0.0.1 alpha",
        context: dict = None,
        command_help=commands.CommandHelp,
        command_version=commands.CommandVersion,
    ):
        self.name = name
        self.version = version
        if context is None:
            context = {}
        self.context = context
        self.options = {}
        self.commands = {}
        if command_help:
            self.add_command(command_help)
        if command_version:
            self.add_command(command_version)

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
        args = [p for p in shlex.split(command_line) if not p.startswith("-")]
        if not args:
            out.critical(10, "No command provided.")
        while args:
            command_name = ".".join(args)
            if command_name in self.commands:
                return self.commands[command_name]
            args.pop()
        return None

    def get_command(self, command_line: str):
        cls = self.find_command(command_line)
        if cls:
            return cls(self, command_line)
        args = [p for p in shlex.split(command_line) if not p.startswith("-")]
        out.critical(20, f'Command "{args[0]}" not found.')

    def launch(self, command_line: str = None):
        try:
            if command_line is None:
                command_line = " ".join(sys.argv[1:])
            cmd = self.get_command(command_line)
            return cmd.launch(command_line)
        except command.CommandException as e:
            out.critical(30, e)
        except command.FieldException as e:
            out.critical(40, e)

    def shell(
        self,
        cmd: str,
        capture_output: bool = True,
        env: dict = None,
        path: str = None,
        shell: bool = True,
    ) -> result.Result:
        if path:
            os.chdir(path)
        env_vars = os.environ.copy()
        if env:
            env_vars.update(env)
        try:
            proc = subprocess.run(
                cmd if shell else shlex.split(cmd),
                shell=shell,
                capture_output=capture_output,
                env=env_vars,
                check=False,
            )
            return result.Result(proc.returncode, proc.stdout, proc.stderr)
        except subprocess.CalledProcessError as e:
            return result.ResultError(e.stderr, e.returncode)
