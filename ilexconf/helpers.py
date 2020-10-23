from typing import Dict, Any


def keyval_to_dict(key: str, value: Any, prefix: str = "", separator: str = "__", lowercase: bool = False) -> Dict:
    """Transform key-value into Mapping.
    """

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
        return {k: keyval_to_dict(subkey, value, prefix="", separator=separator)}

    elif isinstance(parts, list) and len(parts) == 1:
        # Special case for Issue#21
        return {parts[0]: value}

    else:
        return {parts: value}
