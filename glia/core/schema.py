import os

from schema import Optional, Or, Regex, Schema

ENV_MAPPINGS = {
        "bot": {
            "token": "GLIA_TOKEN",
            "debug": "GLIA_DEBUG"
        },
        "database": {
            "host": "GLIA_HOST",
            "port": "GLIA_PORT",
            "username": "GLIA_USERNAME",
            "password": "GLIA_PASSWORD",
            "database": "GLIA_DATABASE"
        },
        "global": {
            "prefixes": "GLIA_PREFIXES",
            "description": "GLIA_DESCRIPTION"
        }
    }

OPTIONAL_ENVS = [
    "GLIA_DESCRIPTION",
    "GLIA_DEBUG"
]


config_schema = Schema(
    {
        'bot': {
            'token': Regex(r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}'),
            'debug': Or(True, False),
            'project': str,
            'plugins_folder': os.path.exists,
            'log_type': Or('Normal', 'Timed')
        },
        'database': {
            # Schema hooks can be used to force driver detail checks
            # as noted in https://git.io/fhhd2 instead of resorting
            # to blanket optionals. Will get to this later if more
            # databases are needed!
            'enabled': Or(True, False),
            Optional('driver'): "mongo",
            Optional('host'): [str],
            Optional('port'): int,
            Optional('username'): str,
            Optional('password'): str,
            Optional('database'): str,
            Optional('replica'): str
        },
        'global': {
            'name': str,
            'icon_url': str,
            'prefixes': [str],
            'description': str
        }
    },
    ignore_extra_keys=True
)


plugin_schema = Schema(
    {
        Optional('name'): str,
        'database': Or(True, False),
    }
)
