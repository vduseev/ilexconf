from typing import Dict


def keyval_to_dict(key, value, prefix="", separator="__", lowercase=False) -> Dict:
    """    Transform key-value into Mapping.    """

    if prefix and not key.startswith(prefix):
            # if prefix is specified, then return nothing for keys without it
            return {}

    # strip key off of prefix
    prefixless_key = key[len(prefix) :]
    # lowercase key if needed
    key = prefixless_key.lower() if lowercase else prefixless_key
    prefix = prefix.lower() if lowercase else prefix

    parts = key.strip(separator).split(separator, maxsplit=1) if separator else key
    if isinstance(parts, list) and len(parts) > 1:
        k, subkey = parts  # unpack split parts for readability
        return {k: keyval_to_dict(subkey, value, prefix=prefix, separator=separator)}
    elif isinstance(parts, list) and len(parts) == 1:
        # Special case for Issue#21
        return {parts[0]: value}
    else:
        print(f"fucking parts is {parts}")
        return {parts: value}
