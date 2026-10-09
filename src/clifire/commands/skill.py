from clifire import command, out, skill


class CommandSkill(command.Command):
    _name = 'skill'
    _help = 'Print, locate or install the AI agent skill file'

    action = command.Field(
        pos=1,
        help='Action: print the content (default), path or install',
        default='print',
    )
    target = command.Field(
        help='Install target: auto, all, project, claude or crush',
        default='auto',
    )

    def fire(self):
        if self.action == 'print':
            print(skill.content())
        elif self.action == 'path':
            print(skill.path())
        elif self.action == 'install':
            self.install()
        else:
            raise command.FieldException(
                self._fields['action'],
                f'has an invalid value "{self.action}"',
            )

    def install(self):
        try:
            written = skill.install(self.target)
        except ValueError:
            raise command.FieldException(
                self._fields['target'],
                f'has an invalid value "{self.target}"',
            ) from None
        for file in written:
            out.success(f'Installed skill file at {file}')
