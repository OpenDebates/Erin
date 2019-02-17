import logging

import coloredlogs

LOG_FORMAT = "%(asctime)s %(name)-18s %(levelname)-8s %(message)s"
DATE_FORMAT = "[%Y-%m-%d %H:%M:%S %z]"
FIELD_STYLES = {
    'asctime': {
        'color': 'green'
    },
    'hostname': {
        'color': 'magenta'
    },
    'levelname': {
        'color': 'black',
        'bold': True
    },
    'name': {
        'color': 170
    },
    'programname': {
        'color': 'cyan'
    }
}


class LogFormatter(coloredlogs.ColoredFormatter):
    def __init__(self):
        super().__init__(
            LOG_FORMAT,
            datefmt=DATE_FORMAT
        )


def setup_custom_logger(name):
    formatter = coloredlogs.ColoredFormatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT,
        field_styles=FIELD_STYLES
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


# Discord Logger
discord_logger = logging.getLogger('discord')
discord_handler = logging.StreamHandler()
discord_logger.setLevel(logging.INFO)
discord_formatter = LogFormatter()
discord_handler.setFormatter(discord_formatter)
discord_logger.addHandler(discord_handler)
