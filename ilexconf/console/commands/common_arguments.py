from cleo import argument as cleo_argument

from ilexconf import Config


common_args = Config()


def _add_arg(arg):
    common_args[arg.name].arg = arg


def argument(name):
    return common_args[name].arg


path = cleo_argument(
    name="path",
    description="[optional] Path to the configuration file.",
    optional=True,
)
_add_arg(path)
