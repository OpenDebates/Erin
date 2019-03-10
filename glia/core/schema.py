import os

from schema import Regex, Schema, And, Or, Use, Optional

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
            'enabled': Or(True, False),
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
