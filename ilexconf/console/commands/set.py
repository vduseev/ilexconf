from cleo import Command, argument, option

from ilexconf.console.options import file, file_type, scopes


class SetCommand(Command):
    name = "set"
    description = "Set value of the key"

    arguments = [
        argument(
            name="key",
            description="Key ('my.key') OR key-value pair ('my.key=231')",
            optional=False,
        ),
        argument(
            name="value",
            description="(optional) Value of the key when <key> argument is just a key name",
            optional=True,
        )
    ]

    options = [
        file,
        file_type,
        *scopes
    ]

    def handle(self):
        print("Wow, you've set it")
