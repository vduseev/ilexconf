from ilexconf.config import Config
from mapz import to_flat
from argparse import Namespace


def from_argparse(args: Namespace):

    config = Config(vars(args))
    return config


def to_argparse(config: Config, prefix=""):

    flat = to_flat(config, prefix=prefix, sep="_")

    args = Namespace()
    for k in flat:
        setattr(args, k, flat[k])

    return args
