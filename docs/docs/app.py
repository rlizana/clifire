import time

from clifire import application, command, out


class OutCommand(command.Command):
    _name = "out"

    def fire(self):
        out.info("This is an informational message")
        out.success("Operation completed successfully")
        out.warn("Warning: check your configuration")
        out.error("Critical error occurred")

        print("")
        print("Debug")
        print("-" * 80)
        out.debug("Debug: variable x = 42")
        sample_dict = {"key": "value", "numbers": [1, 2, 3]}
        out.var_dump(sample_dict)

        print("")
        print("Tables")
        print("-" * 80)
        data = [
            {"name": "Luke", "age": 18, "is_student": True},
            {"name": "Elizabeth", "age": 101, "is_student": False},
        ]
        out.table(data, border=True, title="Contacts")

        print("")
        print("Live text")
        print("-" * 80)
        live_text = out.LiveText("Starting...")
        time.sleep(1)
        live_text.info("Process running")
        time.sleep(1)
        live_text.warn("Retrying operation")
        time.sleep(1)
        live_text.success("Operation completed", end=False)
        time.sleep(1)


def main():
    app = application.App()
    app.add_command(OutCommand)
    app.fire("out -v")


if __name__ == "__main__":
    main()
