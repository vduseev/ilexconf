from cleo import Command, option

from ilexconf.console.options import file_type, scopes


class ConvertCommand(Command):
    name = "convert"
    description = "Convert config from one format to another"

    options = [file_type, *scopes]

    def handle(self):
        print("Nice conversion, my dude. You do that often?")
