import time

from clifire import application, command, out


class CommandInfo(command.Command):
    """
    Show a message text with info style.
    """

    _name = "info"

    text = command.Field(pos=1, help="Message text to show in the console")
    name = command.Field(pos=2, default="", help="A sample name")
    type = command.Field(
        help="Color can be: info, warn or error",
        default="info",
        alias=["t", "color"],
    )

    def fire(self):
        if self.name:
            self.text = f"{self.name}: {self.text}"
        if self.type == "info":
            out.info(self.text)
        elif self.type == "warn":
            out.warn(self.text)
        elif self.type == "error":
            out.error(self.text)
        else:
            out.warn(f'Type "{self.type}" unknow')


class CommandInfoAsk(command.Command):
    """
    Show a message text like a question.
    """

    _name = "info.ask"

    text = command.Field(pos=1, help="Message text to show in the console")
    type = command.Field(
        help="Color can be: info, warn or error",
        default="info",
        alias=["t", "color"],
    )
    end_char = command.Field(
        help="character for end the phrase",
        default="?",
        alias=["char"],
    )

    def fire(self):
        self.text = f"{self.text}{self.end_char}"
        if self.type == "info":
            out.info(self.text)
        elif self.type == "warn":
            out.warn(self.text)
        elif self.type == "error":
            out.error(self.text)
        else:
            out.warn(f'Type "{self.type}" unknow')


class CommandLive(command.Command):
    _name = "live"
    _help = "Show a message text in live mode"

    time = command.Field(pos=1, force_type=int, help="Duration in seconds")

    def fire(self):
        time_sleep = 0.5
        live = out.LiveText("Starting ...")
        time.sleep(time_sleep)
        live.warn("Ready ...")
        time.sleep(time_sleep)
        live.success("Go ...", end=False)
        time.sleep(time_sleep)
        live.error("Trying again ...", end=False)
        time.sleep(time_sleep)
        live.success("Go ...", end=False)
        max_value = self.time
        value = 0
        while value < max_value:
            live.info(f"Count {value} to {max_value}")
            value += 1
            time.sleep(time_sleep)
        live.success(f"Regresive count for {max_value} ended!")


app = application.App(name="Out sample", version="1.0")
app.add_command(CommandInfo)
app.add_command(CommandInfoAsk)
app.add_command(CommandLive)

if __name__ == "__main__":
    app.fire()
