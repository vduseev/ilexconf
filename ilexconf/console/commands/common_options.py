from cleo import option as cleo_option

from ilexconf import Config
from ilexconf.adapters import enabled_formats


common_opts = Config()


def _add_option(o, choices=None):
    common_opts[o.long_name].opt = o
    if choices:
        common_opts[
            o.long_name
        ].opt._description += f"Choices: {', '.join(choices)}."
        common_opts[o.long_name].choices = choices


def option(name):
    if name not in common_opts:
        raise Exception(f"Option {name} was not defined")
    return common_opts[name].opt


filetype = cleo_option(
    long_name="type",
    short_name="t",
    description="File type. ",
    flag=False,
    value_required=True,
)
_add_option(filetype, choices=enabled_formats)

source_filetype = cleo_option(
    long_name="source-type",
    short_name="s",
    description="Source file type. ",
    flag=False,
    value_required=True,
)
_add_option(source_filetype, choices=enabled_formats)

destination_filetype = cleo_option(
    long_name="dest-type",
    short_name="d",
    description="Destination file type. ",
    flag=False,
    value_required=True,
)
_add_option(destination_filetype, choices=enabled_formats)

display = cleo_option(
    long_name="display",
    short_name="d",
    description="Display format of the config. ",
    flag=False,
    value_required=True,
)
_add_option(display, choices=["table"] + enabled_formats)

flatten = cleo_option(
    long_name="flatten",
    description="Flatten config before output",
    flag=True,
    value_required=False,
)
_add_option(flatten)

lowercase = cleo_option(
    long_name="lowercase",
    description="Lowercase config keys",
    flag=True,
    value_required=False,
)
_add_option(lowercase)

uppercase = cleo_option(
    long_name="uppercase",
    description="Uppercase config keys",
    flag=True,
    value_required=False,
)
_add_option(uppercase)

prefix = cleo_option(
    long_name="prefix",
    description="Prefix of the environment variables (default: '')",
    flag=False,
    value_required=True,
    multiple=True,
)
_add_option(prefix)

separator = cleo_option(
    long_name="separator",
    description="Environment variable hierarchical delimiter (default: '__')",
    flag=False,
    value_required=True,
)
_add_option(separator)

env = cleo_option(
    long_name="env",
    short_name="e",
    description="Consider environment variables",
    flag=True,
    value_required=False,
)
_add_option(env)

user = cleo_option(
    long_name="user",
    description="Search for config file in user's scope",
    flag=True,
    value_required=False,
)
_add_option(user)

system = cleo_option(
    long_name="system",
    description="Search for config file in system's scope",
    flag=True,
    value_required=False,
)
_add_option(system)

tree = cleo_option(
    long_name="tree",
    description="Search for config file in the directory hierarchy up to the root",
    flag=True,
    value_required=False,
)
_add_option(tree)
