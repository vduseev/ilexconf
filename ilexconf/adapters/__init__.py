from ilexconf import Config

from ilexconf.adapters.env import from_env, to_env
from ilexconf.adapters.ini import from_ini
from ilexconf.adapters.json import from_json, to_json


formats = Config()

formats.json.enabled = True
formats.json.reader = from_json
formats.json.writer = to_json
formats.json.extensions = ["json"]

formats.yaml.enabled = False
formats.yaml.extensions = ["yaml", "yml"]

enabled_formats = [f for f in formats if formats[f].enabled]
