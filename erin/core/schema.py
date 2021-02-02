import os

from schema import Optional, Or, Schema

ENV_MAPPINGS = {
    "bot": {
        "token": "ERIN_TOKEN",
        "debug": "ERIN_DEBUG",
        "project": "ERIN_PROJECT",
        "project_folder": "ERIN_PROJECT_FOLDER",
        "log_type": "ERIN_LOG_TYPE",
        "log_level": "ERIN_LOG_LEVEL",
    },
    "database": {
        "enabled": "ERIN_DB_ENABLED",
        "driver": "ERIN_DB_DRIVER",
        "uri": "ERIN_DB_URI",
        "host": "ERIN_DB_HOST",
        "port": "ERIN_DB_PORT",
        "username": "ERIN_DB_USERNAME",
        "password": "ERIN_DB_PASSWORD",
        "database": "ERIN_DB_DATABASE",
    },
    "global": {"prefixes": "ERIN_PREFIXES", "description": "ERIN_DESCRIPTION"},
}

OPTIONAL_ENVS = [
    "ERIN_DEBUG",
    "ERIN_DB_DRIVER",
    "ERIN_DB_URI",
    "ERIN_DB_HOST",
    "ERIN_DB_PORT",
    "ERIN_DB_USERNAME",
    "ERIN_DB_PASSWORD",
    "ERIN_DB_DATABASE" "ERIN_DESCRIPTION",
]


config_schema = Schema(
    {
        "bot": {
            "token": str,
            "debug": Or(True, False),
            "project": str,
            "plugins_folder": os.path.exists,
            "log_type": Or("Normal", "Timed"),
            "log_level": Or(
                "SPAM",
                "DEBUG",
                "VERBOSE",
                "INFO",
                "NOTICE",
                "WARNING",
                "SUCCESS",
                "ERROR",
                "CRITICAL",
            ),
        },
        "database": {
            # Schema hooks can be used to force driver detail checks
            # as noted in https://git.io/fhhd2 instead of resorting
            # to blanket optionals. Will get to this later if more
            # databases are needed!
            "enabled": Or(True, False),
            Optional("driver"): "mongo",
            Optional("uri"): str,
            Optional("host"): [str],
            Optional("port"): int,
            Optional("username"): str,
            Optional("password"): str,
            Optional("database"): str,
            Optional("replica"): str,
        },
        "global": {"name": str, "prefixes": [str], "description": str},
    },
    ignore_extra_keys=True,
)


plugin_schema = Schema({Optional("name"): str, "database": Or(True, False)})
