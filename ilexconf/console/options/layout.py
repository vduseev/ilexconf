from cleo import option


layout = option(
    long_name="layout",
    short_name="l",
    description=(
        "Layout format of the output (choices: table, flat, "
        "json, yaml, toml; default: table)"
    ),
    flag=False,
    value_required=True,
)
