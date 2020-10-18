from cleo import Command, argument, option

from ilexconf.console.options import file_type, scopes


class SetCommand(Command):
    name = "set"

    description = "Set value of the key"
    help = "\n".join(
        [
            "",
            "# Set specific value in the config",
            "set settings.json key value",
            "set settings.json key=value",
            "",
            "# Set environment variable in current shell",
            "set key value",
            "set key=value",
        ]
    )

    arguments = [
        argument(
            name="key",
            description="Config key ('my.key') or key-value pair ('my.key=231')",
        ),
        argument(
            name="value",
            description="[optional] Value of the key when <key> argument is just a key name",
            optional=True,
        ),
    ]

    options = [file_type, *scopes]

    def handle(self):
        print("Wow, you've set it")
