from clifire import application, command, out


def output(capsys):
    captured = capsys.readouterr()
    return out.ansi_clean(captured.out)


def test_command_help(capsys):
    app = application.App(name="sample", version="1.0.99")
    app.launch("help")
    printed = output(capsys)
    assert "Description" in printed
    assert "Arguments" in printed
    assert "version" in printed
    assert "help" in printed


def test_command_help_without_arguments(capsys):
    class CommandTest(command.Command):
        _name = "test"
        _help = "Test sample"

    app = application.App(name="sample", version="1.0.99")
    app.add_command(CommandTest)
    app.launch("help test")
    printed = output(capsys)
    assert "Description" in printed
    assert "Arguments" not in printed
