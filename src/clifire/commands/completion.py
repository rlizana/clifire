import os
from typing import Dict, List

from clifire import command, out

SHELLS = ('bash', 'zsh', 'fish')

BASH_TEMPLATE = '''\
_clifire_completion() {
    local cur path="" tok i cmd rest next
    local -a candidates opts
    cur="${COMP_WORDS[COMP_CWORD]}"
    for ((i = 1; i < COMP_CWORD; i++)); do
        tok="${COMP_WORDS[i]}"
        case "$tok" in
            -*) ;;
            *) path="${path}${path:+.}${tok}" ;;
        esac
    done
    for cmd in __COMMANDS__; do
        rest=""
        if [ -n "$path" ]; then
            case "$cmd" in
                "$path") ;;
                "$path".*) rest="${cmd#"$path".}" ;;
                *) continue ;;
            esac
        else
            rest="$cmd"
        fi
        next="${rest%%.*}"
        if [ -n "$next" ]; then
            if [[ " ${candidates[*]} " != *" $next "* ]]; then
                candidates+=("$next")
            fi
        fi
    done
    local -A cmd_opts
__CMD_OPTS__
    opts=(__GLOBAL_OPTS__)
    if [ -n "$path" ]; then
        opts+=(${cmd_opts[$path]})
    fi
    COMPREPLY=($(compgen -W "${candidates[*]} ${opts[*]}" -- "$cur"))
}

complete -F _clifire_completion __BIN__
'''

ZSH_TEMPLATE = '''\
#compdef __BIN__

_clifire_completion() {
    local path="" tok i cmd rest next
    local -a candidates opts
    for ((i = 2; i < CURRENT; i++)); do
        tok="${words[i]}"
        [[ "$tok" == -* ]] && continue
        path="${path}${path:+.}${tok}"
    done
    local -A cmd_opts
__CMD_OPTS__
    for cmd in __COMMANDS__; do
        rest=""
        if [[ -n "$path" ]]; then
            case "$cmd" in
                "$path") ;;
                "$path".*) rest="${cmd#"$path".}" ;;
                *) continue ;;
            esac
        else
            rest="$cmd"
        fi
        next="${rest%%.*}"
        if [[ -n "$next" ]] && (( ! ${candidates[(Ie)$next]} )); then
            candidates+=("$next")
        fi
    done
    opts=(__GLOBAL_OPTS__)
    if [[ -n "$path" ]]; then
        opts+=(${=cmd_opts[$path]})
    fi
    compadd -a candidates opts
}

if (( $+functions[compdef] )); then
    compdef _clifire_completion __BIN__
fi
'''


def _field_flags(field) -> List[str]:
    flags = []
    for name in [field.name] + list(field.alias):
        name = name.replace('_', '-')
        flag = f'-{name}' if len(name) == 1 else f'--{name}'
        if flag not in flags:
            flags.append(flag)
    return flags


def _command_fields(cls) -> List:
    fields = []
    for attr in dir(cls):
        value = getattr(cls, attr)
        if isinstance(value, command.Field):
            value.name = attr
            fields.append(value)
    return fields


def _global_flags(app) -> List[str]:
    options: Dict[str, set] = {}
    for key, value in app.options.items():
        if isinstance(value, str):
            options.setdefault(value, set()).add(key)
        else:
            options.setdefault(key, set())
    flags = []
    for name in options:
        for part in [name] + sorted(options[name]):
            part = part.replace('_', '-')
            flag = f'-{part}' if len(part) == 1 else f'--{part}'
            if flag not in flags:
                flags.append(flag)
    return flags


def _commands_options(app) -> Dict[str, List[str]]:
    result = {}
    for name, cls in sorted(app.commands.items()):
        flags = []
        for field in _command_fields(cls):
            if not field.is_option:
                continue
            for flag in _field_flags(field):
                if flag not in flags:
                    flags.append(flag)
        if flags:
            result[name] = flags
    return result


def _help_of(cls) -> str:
    text = (cls._help or cls.__doc__ or '').strip()
    return text.splitlines()[0] if text else ''


def _cmd_opts_lines(app) -> List[str]:
    lines = []
    for name, flags in _commands_options(app).items():
        joined = ' '.join(flags)
        lines.append(f"    cmd_opts['{name}']='{joined}'")
    return lines


def bash_script(app, bin_name: str = 'fire') -> str:
    script = BASH_TEMPLATE
    script = script.replace('__COMMANDS__', ' '.join(sorted(app.commands)))
    script = script.replace('__GLOBAL_OPTS__', ' '.join(_global_flags(app)))
    script = script.replace('__BIN__', bin_name)
    return script.replace('__CMD_OPTS__', '\n'.join(_cmd_opts_lines(app)))


def zsh_script(app, bin_name: str = 'fire') -> str:
    script = ZSH_TEMPLATE
    script = script.replace('__COMMANDS__', ' '.join(sorted(app.commands)))
    script = script.replace('__GLOBAL_OPTS__', ' '.join(_global_flags(app)))
    script = script.replace('__BIN__', bin_name)
    return script.replace('__CMD_OPTS__', '\n'.join(_cmd_opts_lines(app)))


def _fish_quote(text: str) -> str:
    return text.replace('\\', '\\\\').replace("'", "\\'")


def _fish_option(
    bin_name: str, flags: List[str], desc: str, condition: str = ''
) -> str:
    parts = [f'complete -c {bin_name}']
    if condition:
        parts.append(f"-n '{condition}'")
    for flag in flags:
        if flag.startswith('--'):
            parts.append(f'-l {flag[2:]}')
        else:
            parts.append(f'-s {flag[1:]}')
    if desc:
        parts.append(f"-d '{_fish_quote(desc)}'")
    return ' '.join(parts)


def _fish_condition(segments: List[str]) -> str:
    checks = [f'__fish_seen_subcommand_from {name}' for name in segments]
    return '; and '.join(checks)


def fish_script(app, bin_name: str = 'fire') -> str:
    lines = [f'# fish completion for {bin_name}', '']
    seen = set()
    for name in sorted(app.commands):
        segments = name.split('.')
        if len(segments) == 1:
            condition = '__fish_use_subcommand'
        else:
            condition = _fish_condition(segments[:-1])
        cls = app.commands[name]
        line = _fish_option(bin_name, [], _help_of(cls), condition)
        line = f"{line} -a '{segments[-1]}' -f"
        if line not in seen:
            seen.add(line)
            lines.append(line)
    lines.append('')
    for flag in _global_flags(app):
        lines.append(_fish_option(bin_name, [flag], ''))
    lines.append('')
    for name, cls in sorted(app.commands.items()):
        condition = _fish_condition(name.split('.'))
        for field in _command_fields(cls):
            if not field.is_option:
                continue
            for flag in _field_flags(field):
                line = _fish_option(bin_name, [flag], field.help, condition)
                if line not in seen:
                    seen.add(line)
                    lines.append(line)
    return '\n'.join(lines) + '\n'


def detect_shell() -> str:
    shell = os.environ.get('SHELL', '')
    for name in SHELLS:
        if shell.endswith(name):
            return name
    return 'bash'


def write_script(shell: str, content: str, bin_name: str = 'fire'):
    home = os.path.expanduser('~')
    rc_file = None
    if shell == 'fish':
        folder = os.path.join(home, '.config', 'fish', 'completions')
        dest = os.path.join(folder, f'{bin_name}.fish')
    else:
        folder = os.path.join(home, '.config', 'clifire')
        dest = os.path.join(folder, f'completion.{shell}')
        rc_file = os.path.join(home, f'.{shell}rc')
    os.makedirs(folder, exist_ok=True)
    with open(dest, 'w') as file:
        file.write(content)
    if rc_file is None:
        return dest, None
    line = f'source {dest}'
    current = ''
    if os.path.exists(rc_file):
        with open(rc_file) as file:
            current = file.read()
    if line in current:
        return dest, None
    with open(rc_file, 'a') as file:
        file.write(f'\n{line}\n')
    return dest, line


class CommandCompletion(command.Command):
    _name = 'completion'
    _help = 'Generate shell completion scripts for this application'

    shell = command.Field(
        pos=1,
        help='Shell to generate the script for: bash, zsh or fish',
        default='',
    )
    install = command.Field(
        default=False,
        help='Install the completion script for the current shell',
    )
    bin = command.Field(
        default='fire',
        help='Name of the command to complete (default: fire)',
    )

    def fire(self):
        if self.install:
            self.install_completion()
            return
        if not self.shell:
            raise command.FieldException(
                self._fields['shell'],
                'is required, choose bash, zsh or fish',
            )
        if self.shell not in SHELLS:
            raise command.FieldException(
                self._fields['shell'],
                f'has an invalid value "{self.shell}"',
            )
        print(self.script(self.shell))

    def script(self, shell: str) -> str:
        if shell == 'bash':
            return bash_script(self.app, self.bin)
        if shell == 'zsh':
            return zsh_script(self.app, self.bin)
        return fish_script(self.app, self.bin)

    def install_completion(self):
        shell = detect_shell()
        dest, source = write_script(shell, self.script(shell), self.bin)
        out.success(f'Completion script installed at {dest}')
        if source:
            out.info(f'Line added to your shell rc file: {source}')
        else:
            out.info('Restart your shell to enable completions')
