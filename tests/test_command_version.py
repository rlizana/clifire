from clifire import application, command, out


def output(capsys):
    captured = capsys.readouterr()
    return out.ansi_clean(captured.out)


def test_command_version(capsys):
    app = application.App(name="sample", version="1.0.99")
    app.fire("version")
    assert "sample 1.0.99" in output(capsys)


def test_command_version_overwrite(capsys):
    class CommandVersion(command.Command):
        _name = "version"

        def fire(self):
            out.info("Overwrite version message")

    app = application.App(
        name="sample", version="1.0.99", command_version=CommandVersion
    )
    app.fire("version")
    assert "Overwrite version message" in output(capsys)
