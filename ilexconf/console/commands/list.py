from cleo import Command
from pathlib import Path

from ilexconf.config import Config
from ilexconf.adapters import formats, from_env, to_json

from .common_arguments import argument
from .common_options import option


class ListCommand(Command):
    name = "list"

    description = "List configuration file"
    help = "\n".join(
        [
            "",
            "Show contents of the settings.json file as a table",
            "(file format is guessed based on extension):",
            "",
            "    <info>show settings.json</info>",
            "",
            "Show contents of my.conf file but explicitly state",
            "that it contains YAML:",
            "",
            "    <info>show my.conf -t yaml</info>",
            "",
            "Show this help message:",
            "",
            "    <info>show --help</info>",
        ]
    )

    arguments = [argument("path")]
    options = [
        option("type"),
        option("display"),
        option("flatten"),
        option("env"),
        option("prefix"),
        option("separator"),
        option("lowercase"),
        option("uppercase"),
        # option("user"),
        # option("system"),
        # option("tree")
    ]

    aliases = ["show", "print", "describe"]

    def handle(self):
        config = Config()

        filetype = None
        filename = self.argument("path")
        if filename:
            path = Path(filename)

            filetype = self.option("type")
            if filetype and filetype in formats:
                # Use specified filetype if the option was passed
                filetype = formats[filetype]

            elif path.suffix:
                # If file has an extension, try to use to guess the file type
                filetype = self._guess_format_by_suffix(path.suffix)

            if not filetype:
                self.line("<error>Could not determine file type</error>")
                exit()

            try:
                file_config = filetype.reader(filename, read_from_file=True)
                config.merge(file_config)
            except Exception as e:
                self.line(
                    f"<error>Could not parse {filename} file: {e}</error>"
                )
                exit()

        if self.option("env"):
            prefixes = self.option("prefix") or [""]
            for prefix in prefixes:
                params = {"prefix": prefix}
                if self.option("separator"):
                    params["separator"] = self.option("separator")

                try:
                    env_config = from_env(**params)
                    config.merge(env_config)
                except Exception as e:
                    self.line(
                        "<error>Could not parse environment variables</error>"
                    )
                    exit()

        # Flatten configuration if requested
        if self.option("flatten"):
            config = config.flatten()

        if self.option("uppercase"):
            config = config.upper()

        if self.option("lowercase"):
            config = config.lower()

        # Make sure we have a default writer
        writer = filetype.writer if filetype else to_json

        # Print results using the writer
        output = writer(config)
        self.line(output)

    def _guess_format_by_suffix(self, suffix: str):
        extension = suffix.strip(".")
        # Build inverted index that maps each extension -> format
        extension_matching = {
            ext: formats[f]
            for f in formats
            for ext in formats[f].extensions
            if formats[f].enabled
        }

        # Guess file format using extension and inverted index
        return (
            extension_matching[extension]
            if extension in extension_matching
            else None
        )
