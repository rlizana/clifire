import inspect
import re
import shlex
from typing import List, Optional, Type, Union

from clifire import out


def get_current_app():
    from clifire import application

    return application.App.current_app


def fire(func):
    def wrapper(*args, **kwargs):
        cmd = args[0]
        signature = inspect.signature(func)
        for arg in list(signature.parameters.keys())[1:]:
            var = arg[1:] if arg.startswith('_') else arg
            if hasattr(cmd, var):
                kwargs[arg] = getattr(cmd, var)
        return func(*args, **kwargs)

    command_name = getattr(func, '_command_name', func.__name__)
    command_name = re.sub(r'([A-Z_])', '.', command_name).lower()
    class_name = ''.join(
        word.capitalize() for word in command_name.split('.') if word
    )
    doc = (func.__doc__ or '').strip()
    attrs = {
        '_name': command_name,
        '_help': doc.splitlines()[0] if doc.splitlines() else doc,
        'fire': wrapper,
    }
    signature = inspect.signature(func)
    pos = 0
    helps = {k: [] for k in list(signature.parameters.keys())[1:]}
    doc = [d.strip() for d in doc.splitlines() if d]
    current_help = False
    while doc:
        line = doc.pop(0)
        parts = line.split(':')
        if parts[0] in helps:
            current_help = parts[0]
            line = parts[1]
        if not current_help:
            continue
        helps[current_help].append(line.strip())
    for name, param in list(signature.parameters.items())[1:]:
        pos += 1
        var_name = name[1:] if name.startswith('_') else name
        attrs[var_name] = Field(
            pos=None if name.startswith('_') else pos,
            help=' '.join(helps.get(name, '')),
            default=param._default,
            force_type=param._annotation,
            alias=[var_name[0]],
        )
    class_command = type(class_name, (Command,), attrs)
    app = get_current_app()
    app.add_command(class_command)
    return wrapper


class Field:
    def __init__(
        self,
        pos: int = False,
        help: str = '',
        default: str = None,
        alias: Union[str, List[str], None] = None,
        force_type: Optional[Type] = None,
    ):
        self.name = 'unknow'
        self.pos = pos
        self.help = help
        alias = [] if alias is None else alias
        self.alias = [alias] if isinstance(alias, str) else alias
        self.default = default
        self.value = default
        self.is_option = bool(pos is False or pos is None)
        self.is_required = default is None
        if force_type is None:
            if self.default is not None:
                force_type = type(self.default)
            elif self.is_option:
                force_type = bool
            else:
                force_type = str
        self.type = force_type

    def convert(self, value):
        try:
            if self.type == list:
                return value.split(',')
            elif self.type == bool and value is None:
                return True if self.default is None else not self.default
            return self.type(value)
        except Exception as exc:
            msg = f'with he value "{value}" must be {self.type.__name__}'
            raise FieldException(self, msg) from exc


class FieldException(Exception):
    def __init__(self, field: Field, msg: str):
        self.field = field
        field_type = 'option' if self.field.is_option else 'argument'
        super().__init__(f'The {field_type} "{field.name}" {msg}')


class Command:
    _name = ''
    _help = None

    def __init__(self, app, command_line: str = ''):
        self._fields = {}
        self._argument_names = []
        self._options = {}
        self.app = app
        self._fields_update()
        self.command_line = command_line
        self.extra_args = []
        self.init()

    @property
    def context(self):
        return self.app.context

    def _fields_update(self):
        for name in dir(self):
            field = getattr(self, name)
            if isinstance(field, Field):
                field.name = name
                self._fields[name] = field
        self._argument_names = sorted(
            [key for key, val in self._fields.items() if not val.is_option],
            key=lambda k: self._fields[k].pos,
        )
        self._options = {}
        for name, field in self._fields.items():
            if not field.is_option:
                continue
            self._options[name] = field
            for alias in field.alias:
                if alias.startswith('-'):
                    alias = alias[2:] if alias.startswith('--') else alias[1:]
                alias = alias.replace('-', '_')
                if alias in self._options:
                    raise CommandException(f'Duplicate option alias "{alias}"')
                self._options[alias] = name

    def _fields_check(self):
        for name, field in self._fields.items():
            value = getattr(self, name)
            if isinstance(value, Field):
                if field.is_required:
                    raise FieldException(field, 'is required')
                setattr(self, name, field.default)

    def _parse_command_line(self, command_line: str):
        out.debug(f'Parse command line: {command_line}')
        tokens = shlex.split(command_line)
        command_parts = self._name.split('.')
        argument_index = 0
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token in command_parts:
                command_parts.remove(token)
                index += 1
            elif token.startswith('-'):
                consumed = self._handle_option(tokens, index)
                index += consumed
            else:
                consumed = self._handle_argument(tokens, index, argument_index)
                if consumed > 0:
                    argument_index += 1
                    index += consumed
                else:
                    self.extra_args.append(token)
                    index += 1

    def _handle_option(self, tokens: List[str], index: int) -> int:
        token = tokens[index]
        option_str = token[2:] if token.startswith('--') else token[1:]
        name, value = (
            option_str.split('=', 1)
            if '=' in option_str
            else (option_str, None)
        )
        name = name.replace('-', '_')
        option_field = self._find_option(name)
        if not option_field:
            self.extra_args.append(token)
            return 1
        consumed = 1
        if value is None and option_field['field'].type != bool:
            next_token = tokens[index + 1] if index + 1 < len(tokens) else None
            if not next_token.startswith('-'):
                value = next_token
                consumed = 2
        parsed_value = option_field['field'].convert(value)
        option_name = option_field['name']
        if option_field['is_global']:
            self.app.set_option(option_name, parsed_value)
            out.debug2(f'Global option "{option_name}" = {parsed_value}')
        else:
            setattr(self, option_name, parsed_value)
            out.debug2(f'Option "{option_name}" = {parsed_value}')
        return consumed

    def _find_option(self, name: str) -> dict:
        def _get_options(name: str) -> dict:
            if name in self.app.options:
                return self.app.options
            if name in self._options:
                return self._options
            return {}

        options = _get_options(name)
        if not options:
            return None
        field_name = options[name] if isinstance(options[name], str) else name
        return {
            'field': options[field_name],
            'name': field_name,
            'is_global': name in self.app.options,
        }

    def _handle_argument(
        self, tokens: List[str], index: int, argument_index: int
    ) -> int:
        if argument_index >= len(self._argument_names):
            return 0
        field_name = self._argument_names[argument_index]
        field = self._fields[field_name]
        if field.type == list:
            list_values = []
            consumed = 0
            for i in range(index, len(tokens)):
                token = tokens[i]
                list_values.append(token)
                consumed += 1
            setattr(self, field_name, list_values)
            out.debug2(f'Argument "{field_name}" = {list_values}')
            return consumed
        token = tokens[index]
        value = field.convert(token)
        setattr(self, field_name, value)
        out.debug2(f'Argument "{field_name}" = {value}')
        return 1

    def parse(self, command_line: str):
        self._parse_command_line(command_line)
        self._fields_check()

    def launch(self, command_line: str):
        self.command_line = command_line
        out.debug(f'Launching command "{self._name}"')
        self.parse(command_line)
        out.debug(f'Running command "{self._name}"')
        return self.fire()

    def init(self):
        pass

    def fire(self):
        raise NotImplementedError


class CommandException(Exception):
    pass
