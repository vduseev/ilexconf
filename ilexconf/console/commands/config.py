from cleo import Command

from .list import ListCommand

# from .get import GetCommand
# from .set import SetCommand
# from .convert import ConvertCommand


class ConfigCommand(Command):
    name = "config"
    description = "Configuration command"

    commands = [
        ListCommand(),
        # GetCommand(),
        # SetCommand(),
        # ConvertCommand(),
    ]

    def handle(self):
        return self.call("help", self._config.name)
