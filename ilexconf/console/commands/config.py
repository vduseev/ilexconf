from cleo import Command

from ilexconf.console.commands.show import ShowCommand
from ilexconf.console.commands.get import GetCommand
from ilexconf.console.commands.set import SetCommand
from ilexconf.console.commands.convert import ConvertCommand


class ConfigCommand(Command):
    name = "config"
    description = "Configuration command"

    commands = [
        ShowCommand(),
        GetCommand(),
        SetCommand(),
        ConvertCommand(),
    ]

    def handle(self):
        return self.call("help", self._config.name)
