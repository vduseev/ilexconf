from ilexconf.config import Config
from mapz import to_flat
from argparse import Namespace


def from_argparse(args: Namespace, ignore_null: bool = True):
    
    data = vars(args)
    if ignore_null:
        data = { k: v for k, v in data.items() if v is not None }

    config = Config(data)
    return config


def to_argparse(config: Config, prefix=""):

    flat = to_flat(config, prefix=prefix, sep="_")

    args = Namespace()
    for k in flat:
        # TODO: deal with keys that were non-string, like frozensets
        setattr(args, k, flat[k])

    return args
