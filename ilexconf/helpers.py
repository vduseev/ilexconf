from typing import Dict


def keyval_to_dict(key, value, prefix="", separator="__") -> Dict:
    """
    Transform key-value into Mapping.
    """
    parts = key.strip(separator).split(separator, maxsplit=1)
    if len(parts) > 1:
        k, subkey = parts  # unpack split parts for readability
        return {k: keyval_to_dict(subkey, value, prefix=prefix, separator=separator)}
    else:
        return {parts[0]: value}
