import os

from schema import Optional, Or, Regex, Schema

ENV_MAPPINGS = {
        "bot": {
            "token": "ERIN_TOKEN",
            "debug": "ERIN_DEBUG"
        },
        "database": {
            "host": "ERIN_HOST",
            "port": "ERIN_PORT",
            "username": "ERIN_USERNAME",
            "password": "ERIN_PASSWORD",
            "database": "ERIN_DATABASE"
        },
        "global": {
            "prefixes": "ERIN_PREFIXES",
            "description": "ERIN_DESCRIPTION"
        }
    }

OPTIONAL_ENVS = [
    "ERIN_DESCRIPTION",
    "ERIN_DEBUG"
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
            # to blanket optionals. Will get to this later!
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
