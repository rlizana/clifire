from clifire import application, command, out


class HelloCommand(command.Command):
    _name = "hello"
    _help = "Create template"

    title = command.Field(
        pos=1,
        force_type=str,
    )

    def fire(self):
        print(self.title)
        content = self.app.template.render(
            "hello.jinja2", title=self.title, numbers=[1, 2, 3]
        )
        out.success(content)


def main():
    app = application.App(template_folder="./sample_template")
    app.add_command(HelloCommand)
    app.fire()


if __name__ == "__main__":
    main()
