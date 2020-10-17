from cleo import option


prefix = option(
    long_name="prefix",
    short_name="p",
    description="Prefix of the environment variables (default: '')",
)

delimiter = option(
    long_name="delimiter",
    short_name="d",
    description="Environment variable hierarchical delimiter (default: '__')",
)

no_env = option(
    long_name="no-env",
    short_name="E",
    description="Ignore environment variables",
    flag=True,
    value_required=False,
)

env = (prefix, delimiter, no_env)
