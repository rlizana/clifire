from typing import Optional

EXIT_OK = 0
EXIT_NO_COMMAND = 10
EXIT_COMMAND_NOT_FOUND = 20
EXIT_COMMAND = 30
EXIT_FIELD = 40


class CommandError(Exception):
    code = 1

    def __init__(self, message: str = '', code: Optional[int] = None):
        super().__init__(message)
        if code is not None:
            self.code = code


class CommandException(CommandError):
    code = EXIT_COMMAND


class FieldException(CommandError):
    code = EXIT_FIELD

    def __init__(self, field, msg: str):
        self.field = field
        field_type = 'option' if field.is_option else 'argument'
        super().__init__(f'The {field_type} "{field.name}" {msg}')
