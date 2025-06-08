from clifire import application, command, out


class ConfigCommand(command.Command):
    _name = "config"
    _help = "Show config vars"

    def fire(self):
        self.app.config.my_new_var = "My new var"
        out.var_dump(self.app.config)


def main():
    app = application.App(config_files=["~/.myapp.yml"], config_create=True)
    app.add_command(ConfigCommand)
    app.fire()


if __name__ == "__main__":
    main()
