import sys

import pytest

from clifire import application, command, out


class CommandContact(command.Command):
    _name = "contact"

    name = command.Field(
        pos=1,
        help="Then contact name for show in console",
    )
    age = command.Field(
        pos=2,
        help="Then contact age",
        default=18,
    )
    option = command.Field(
        help="Sample option",
        default=False,
    )
    int_option = command.Field(
        help="Int option sample",
        default=1,
        alias=["o", "int"],
    )
    str_option = command.Field(
        help="Str option sample",
        default="default",
        alias=["str"],
    )

    def init(self):
        self.option_init = command.Field(
            help="One dynamic option",
            default="dynamic",
        )

    def run(self):
        out.info(f"Contact {self.name} with {self.age} years old")
        return True


def output(capsys):
    captured = capsys.readouterr()
    return out.ansi_clean(captured.out)


def test_command():
    app = application.App()
    cmd = command.Command(app)
    with pytest.raises(NotImplementedError):
        cmd.launch("")


def test_command_no_name():
    class CommandNoName(command.Command):
        pass

    app = application.App()
    with pytest.raises(command.CommandException):
        app.add_command(CommandNoName)


def test_command_exception(capsys):
    class CommandTest(command.Command):
        _name = "test"

        def run(self):
            raise command.CommandException("Test exception")

    app = application.App()
    app.add_command(CommandTest)
    try:
        app.launch("test")
    except SystemExit as e:
        assert e.code == 30
        assert "Test exception" in output(capsys)


def test_command_not_exists(capsys):
    app = application.App()
    try:
        app.launch("NotExist")
    except SystemExit as e:
        assert e.code == 20
        assert 'Command "NotExist" not found.' in output(capsys)

    app.add_command(CommandContact)
    try:
        app.get_command("")
    except SystemExit as e:
        assert e.code == 10
        assert "No command provided." in output(capsys)

    try:
        app.get_command("--option")
    except SystemExit as e:
        assert e.code == 10
        assert "No command provided." in output(capsys)


def test_command_run(capsys):
    app = application.App()
    app.add_command(CommandContact)
    app.launch("contact NAME")
    assert "Contact NAME " in output(capsys)

    argv = sys.argv
    try:
        sys.argv = ["/tmp", "contact", "TEST_NAME"]
        app.launch()
    finally:
        sys.argv = argv


def test_command_argument(capsys):
    app = application.App()
    app.add_command(CommandContact)

    try:
        app.launch("contact")
    except SystemExit as e:
        assert e.code == 40
        assert 'The argument "name" is required' in output(capsys)

    cmd = app.get_command("contact")
    with pytest.raises(command.FieldException) as ex:
        cmd.launch("contact")
    assert 'The argument "name" is required' == str(ex.value)
    with pytest.raises(command.FieldException) as ex:
        cmd.launch("contact --option")
    assert 'The argument "name" is required' == str(ex.value)
    with pytest.raises(command.FieldException) as ex:
        cmd.launch("contact --option=option_value")
    assert 'The argument "name" is required' == str(ex.value)

    app.launch("contact NAME")
    assert "Contact NAME" in output(capsys)
    app.launch("contact NAME --option")
    assert "Contact NAME" in output(capsys)
    app.launch("contact NAME --option=option_value")
    assert "Contact NAME" in output(capsys)
    app.launch("contact NAME")
    assert "Contact NAME" in output(capsys)

    cmd = app.get_command("contact")
    cmd.parse("contact NAME")
    assert cmd.name == "NAME"
    assert cmd.age == 18

    cmd.parse("contact NAME 20")
    assert cmd.name == "NAME"
    assert isinstance(cmd.age, int)
    assert cmd.age == 20

    cmd.parse("contact NAME --option=option 20")
    assert cmd.name == "NAME"
    assert isinstance(cmd.age, int)
    assert cmd.age == 20

    cmd.parse("contact NAME --option 20")
    assert cmd.name == "NAME"
    assert isinstance(cmd.age, int)
    assert cmd.age == 20

    cmd.parse("contact NAME --option 20 10")
    assert cmd.name == "NAME"
    assert isinstance(cmd.age, int)
    assert cmd.age == 20


def test_command_options():
    app = application.App()
    app.add_command(CommandContact)

    cmd = app.get_command("contact")
    cmd.parse("contact NAME --option")
    assert hasattr(cmd, "option")
    assert cmd.option is True
    assert not hasattr(cmd, "option_init")
    cmd.init()
    assert hasattr(cmd, "option_init")

    cmd = app.get_command("contact")
    cmd.parse("contact --str-option OPT NAME")
    assert cmd.str_option == "OPT"

    cmd = app.get_command("contact")
    cmd.parse("contact NAME --str OPT")
    assert cmd.str_option == "OPT"

    cmd = app.get_command("contact")
    cmd.parse("contact --option NAME --str=OPT --int-option 99 10")
    assert cmd.option is True
    assert cmd.str_option == "OPT"
    assert cmd.int_option == 99
    assert cmd.age == 10

    cmd = app.get_command("contact")
    cmd.parse("contact --str=OPT NAME --int 99 10")
    assert cmd.str_option == "OPT"
    assert cmd.int_option == 99
    assert cmd.age == 10

    cmd = app.get_command("contact")
    cmd.parse("contact --option=OPT --int-option 99 NAME")
    assert cmd.option is True
    assert cmd.str_option == "default"
    assert cmd.int_option == 99
    assert cmd.age == 18

    cmd = app.get_command("contact")
    cmd.parse("contact --str=OPT -o 99 NAME")
    assert cmd.str_option == "OPT"
    assert cmd.int_option == 99

    cmd = app.get_command("contact")
    cmd.parse("contact --str=OPT --o 99 NAME")
    assert cmd.str_option == "OPT"
    assert cmd.int_option == 99

    cmd = app.get_command("contact")
    cmd.parse("contact --str=OPT --o 99 NAME --not-exist-option")
    assert cmd.str_option == "OPT"
    assert cmd.int_option == 99


def test_command_option_list():
    class CommandTest(CommandContact):
        list_option = command.Field(
            help="Sample list option",
            default=[],
            alias="list",
        )

    app = application.App()
    app.add_command(CommandTest)

    cmd = app.get_command("contact")
    cmd.parse("contact NAME --list=one,two,three")
    assert cmd.name == "NAME"
    assert isinstance(cmd.list_option, list)
    assert cmd.list_option == ["one", "two", "three"]


def test_command_option_list_force_type():
    class CommandTest(CommandContact):
        list_option = command.Field(
            help="Sample list option",
            default="a list",
            alias="list",
            force_type=list,
        )

    app = application.App()
    app.add_command(CommandTest)

    cmd = app.get_command("contact")
    cmd.parse("contact NAME --list=one,two,three")
    assert cmd._fields["list_option"].type == list
    assert isinstance(cmd.list_option, list)
    assert cmd.list_option == ["one", "two", "three"]


def test_command_option_default_type():
    class CommandTest(CommandContact):
        bool_option = command.Field(
            help="Sample bool option",
        )

    app = application.App()
    app.add_command(CommandTest)

    cmd = app.get_command("contact")
    cmd.parse("contact NAME --bool-option")
    assert cmd._fields["bool_option"].type == bool
    assert isinstance(cmd.bool_option, bool)
    assert cmd.bool_option is True


def test_command_option_int_convert_error(capsys):
    app = application.App()
    app.add_command(CommandContact)

    with pytest.raises(command.FieldException):
        cmd = app.get_command("contact")
        cmd.parse("contact NAME --int ONE")

    try:
        app.launch("contact NAME --int ONE")
    except SystemExit as e:
        assert e.code == 40
        assert (
            'The option "int_option" with he value "ONE" must be int'
            in output(capsys)
        )


def test_command_option_alias():
    class CommandTest(CommandContact):
        bool_option = command.Field(help="Sample bool option", alias="--bool")

    app = application.App()
    app.add_command(CommandTest)

    cmd = app.get_command("contact")
    cmd.parse("contact NAME --bool")
    assert cmd.bool_option is True


def test_command_option_alias_duplicate(capsys):
    class CommandTest(CommandContact):
        bool_option = command.Field(help="Sample bool option", alias="-o")

    app = application.App()
    app.add_command(CommandTest)
    try:
        app.launch("contact NAME -o")
    except SystemExit as e:
        assert e.code == 30
        assert 'Duplicate option alias "o"' in output(capsys)


def test_command_option_global(capsys):
    class CommandTest(command.Command):
        _name = "test"

        bool_option = command.Field(
            help="Sample bool option",
            alias="-o",
            default=False,
        )

    app = application.App()
    app.add_command(CommandTest)
    app.add_option(
        "verbose",
        command.Field(
            help="Verbose mode",
            default=False,
            alias=["v", "vv", "vvv"],
        ),
    )
    app.add_option(
        "user",
        command.Field(
            help="Username for tests",
            default="ubuntu",
            alias=["-u", "--username"],
        ),
    )
    with pytest.raises(command.CommandException):
        app.add_option(
            "version",
            command.Field(
                help="Show version",
                default="1.0",
                alias=["-v"],
            ),
        )

    assert app.get_option("verbose") is False
    assert app.get_option("not-exists", 99) == 99
    assert app.set_option("not-exists", 99) is False
    cmd = app.get_command("test")
    cmd.parse("test -v -o")
    assert cmd.bool_option is True
    assert app.get_option("verbose") is True
    assert app.get_option("user") == "ubuntu"
    cmd.parse("test -v -o --user=root")
    assert cmd.bool_option is True
    assert app.get_option("verbose") is True
    assert app.get_option("user") == "root"
    cmd.parse("test -v -o --user root")
    assert cmd.bool_option is True
    assert app.get_option("verbose") is True
    assert app.get_option("user") == "root"
