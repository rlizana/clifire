import pytest

from clifire import application, command, errors
from tests.test_output import output


@pytest.fixture(autouse=True)
def reset_current_app():
    application.App.current_app = None
    yield


def test_exit_code_constants():
    assert errors.EXIT_OK == 0
    assert errors.EXIT_NO_COMMAND == 10
    assert errors.EXIT_COMMAND_NOT_FOUND == 20
    assert errors.EXIT_COMMAND == 30
    assert errors.EXIT_FIELD == 40


def test_exception_codes():
    assert errors.CommandError('x').code == 1
    assert errors.CommandError('x', code=55).code == 55
    assert errors.CommandException('x').code == errors.EXIT_COMMAND
    field = command.Field(default=1)
    field.name = 'sample'
    exception = errors.FieldException(field, 'boom')
    assert exception.code == errors.EXIT_FIELD
    assert str(exception) == 'The option "sample" boom'


def test_command_module_aliases():
    assert command.CommandException is errors.CommandException
    assert command.FieldException is errors.FieldException


def test_no_command_exit():
    app = application.App(command_help=None)
    with pytest.raises(SystemExit) as excinfo:
        app.get_command('')
    assert excinfo.value.code == errors.EXIT_NO_COMMAND


def test_command_not_found_exit(capsys):
    app = application.App()
    with pytest.raises(SystemExit) as excinfo:
        app.get_command('nope')
    assert excinfo.value.code == errors.EXIT_COMMAND_NOT_FOUND
    printed = output(capsys)
    assert 'Command "nope" not found.' in printed


def test_custom_command_error(capsys):
    class FailCommand(command.Command):
        _name = 'failcmd'

        def fire(self):
            raise errors.CommandError('boom', code=55)

    app = application.App()
    app.add_command(FailCommand)
    with pytest.raises(SystemExit) as excinfo:
        app.fire('failcmd')
    assert excinfo.value.code == 55
    printed = output(capsys)
    assert 'boom' in printed
