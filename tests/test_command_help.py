from clifire import application, command, out


def output(capsys):
    captured = capsys.readouterr()
    return out.ansi_clean(captured.out)


def test_command_help(capsys):
    app = application.App(name="sample", version="1.0.99")
    app.fire("help")
    printed = output(capsys)
    assert "Description" in printed
    assert "Arguments" in printed
    assert "version" in printed
    assert "help" in printed


def test_command_help_without_help(capsys):
    class CommandTest(command.Command):
        _name = "test_no_help"

    app = application.App()
    app.add_command(CommandTest)
    cmd = app.get_command("test_no_help")
    assert cmd._name == "test_no_help"
    assert cmd._help is None
    app.fire("help test_no_help")
    printed = output(capsys)
    assert "test_no_help" in printed


def test_command_help_without_arguments(capsys):
    class CommandTest(command.Command):
        _name = "test"
        _help = "Test sample"

    app = application.App(name="sample", version="1.0.99")
    app.add_command(CommandTest)
    app.fire("help test")
    printed = output(capsys)
    assert "Description" in printed
    assert "Arguments" not in printed


def test_command_help_without_global_options(capsys):
    app = application.App(
        name="sample", version="1.0.99", option_verbose=False
    )
    app.fire("help")
    printed = output(capsys)
    assert "Description" in printed
    assert "Global options:" not in printed
    assert "Arguments" in printed
    assert "version" in printed
    assert "help" in printed


def test_command_help_with_groups(capsys):
    class CommandDbCreate(command.Command):
        _name = "db.create"
        _help = "Create database"

    class CommandDbDrop(command.Command):
        _name = "db.drop"
        _help = "Drop database"

    class CommandConfigSet(command.Command):
        _name = "config.set"
        _help = "Set config value"

    app = application.App(name="sample", version="1.0.99")
    app.add_command(CommandDbCreate)
    app.add_command(CommandDbDrop)
    app.add_command(CommandConfigSet)

    app.fire("help")
    printed = output(capsys)
    assert "db" in printed
    assert "config" in printed

    assert "create" in printed
    assert "drop" in printed
    assert "set" in printed

    assert "Create database" in printed
    assert "Drop database" in printed
    assert "Set config value" in printed

    db_pos = printed.find("db")
    config_pos = printed.find("config")
    assert config_pos < db_pos
