from cleo import option


user = option(
    long_name="user",
    description="Search for config file in user's scope",
    flag=True,
    value_required=False,
)

system = option(
    long_name="system",
    description="Search for config file in system's scope",
    flag=True,
    value_required=False,
)

tree = option(
    long_name="tree",
    description="Search for config file in the directory hierarchy up to the root",
    flag=True,
    value_required=False,
)

scopes = (user, system, tree)
