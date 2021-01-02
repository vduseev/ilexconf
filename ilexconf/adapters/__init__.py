from .env import from_env, to_env
from .ini import from_ini, to_ini
from .json import from_json, to_json
from .argparse import from_argparse, to_argparse

try:
    from .yaml import from_yaml, to_yaml

    yaml_here = True
except ImportError:  # pragma: no cover
    yaml_here = False
    from_yaml = None
    to_yaml = None


# formats.json = {
#     "enabled": True,
#     "reader": from_json,
#     "writer": to_json,
#     "extensions": ["json"],
# }

# formats.yaml = {"enabled": yaml_here, "extensions": ["yaml", "yml"]}
# if yaml_here:  # pragma: no cover
#     formats.yaml.reader = from_yaml
#     formats.yaml.writer = to_yaml

enabled_formats = ['json', 'yaml']
