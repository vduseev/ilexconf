try:
    from ruamel.yaml import YAML
    yaml = YAML()
except ImportError:
    try:
        import pyyaml as yaml
    except ImportError:
        yaml = None

from .common.decorators import reader, writer


if yaml:
    def _load(data: str):
        # If data is a string in a form of
        # "name: boris" or "name:" then it will
        # be parsed by yaml module to a str instance.
        d = yaml.load(data)

        # Do not accept plain string yaml files
        # as configs. Treat such strings as paths.
        if isinstance(d, str):
            with open(data, "rt") as f:
                d = yaml.load(f)
        
        return d


    @reader(load=_load)
    def from_yaml():
        """Read data from YAML string, file object or path"""
        pass  # pragma: no cover


    @writer(dump=lambda data: yaml.dump(data))
    def to_yaml():
        """Write data to YAML file or convert to YAML string"""
        pass  # pragma: no cover
