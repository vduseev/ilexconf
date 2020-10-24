try:
    from ruamel.yaml import YAML
    yaml = YAML()
except ImportError:
    try:
        import pyyaml as yaml
    except ImportError:
        yaml = None

from .decorators import reader, writer


if yaml:
    def _string_loader(data: str):
        d = yaml.load(data)

        # Do not accept plain string yaml files
        # as configs. Treat such string as path.
        if isinstance(d, str):
            with open(data, "rt") as f:
                d = yaml.load(f)
        
        return d


    @reader(
        file_load=lambda data: yaml.load(data),
        path_load=lambda data: yaml.load(data.open("rt")),
        string_load=_string_loader
    )
    def from_yaml():
        """Read data from YAML string, file object or path"""
        pass  # pragma: no cover


    @writer(
        dump=lambda data: yaml.dump(data)
    )
    def to_yaml():
        """Write data to YAML file or convert to YAML string"""
        pass  # pragma: no cover
