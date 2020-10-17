from cleo import option


file = option(
    long_name="file",
    short_name="f",
    description=(
        "Path to the configuration file. When omitted, "
        "command only interacts with environment variables in current context."
    )
)

output = option(
    long_name="output",
    short_name="o",
    description="Path to the output file"
)

file_type = option(
    long_name="type",
    short_name="t",
    description=(
        "File type of the configuration (default: "
        "ilexconf tries to guess file type by extension)"
    ),
    flag=False,
    value_required=True,
)

io = (file, output, file_type)
