from cleo import Command, argument, option

from ilexconf.console.options import file, file_type, scopes


class GetCommand(Command):
    name = "get"
    description = "Get value from the configuration"

    arguments = [
        argument(
            name="key",
            description="Key to retrieve",
            optional=False,
        )
    ]

    options = [
        file,
        file_type,
        *scopes
    ]

    def handle(self):
        print("Here comes value")
