from cleo import Command, argument, option

from ilexconf.config import Config
from ilexconf.adapters.env import from_env
from ilexconf.console.options import file, file_type, layout, scopes, env


class ShowCommand(Command):
    name = "show"
    description = "Show configuration file"

    options = [
        file,
        layout,
        file_type,
        *env, 
        *scopes
    ]

    def handle(self):
        print("Show")
