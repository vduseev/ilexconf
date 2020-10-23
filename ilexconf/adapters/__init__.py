from ilexconf.config import Config

from .env import from_env, to_env
from .ini import from_ini, to_ini
from .json import from_json, to_json

try:
    from .yaml import from_yaml, to_yaml
    yaml_here = True
except ImportError:
    yaml_here = False
    from_yaml = None
    to_yaml = None


formats = Config()
formats.json = {
    "enabled": True,
    "reader": from_json,
    "writer": to_json,
    "extensions": ["json"]
}

formats.yaml = {
    "enabled": yaml_here,
    "extensions": ["yaml", "yml"]
}
if yaml_here:
    formats.yaml.reader = from_yaml
    formats.yaml.writer = to_yaml

enabled_formats = [f for f in formats if formats[f].enabled]
