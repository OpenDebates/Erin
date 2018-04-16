import logging
from logging import getLoggerClass, NOTSET, addLevelName


discord_logger = logging.getLogger('discord')
discord_handler = logging.StreamHandler()
discord_logger.setLevel(logging.INFO)
discord_formatter = logging.Formatter(
    '%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
    datefmt="[%Y-%m-%d %H:%M:%S %z]"
)
discord_handler.setFormatter(discord_formatter)
discord_logger.addHandler(discord_handler)


class BotLogger(getLoggerClass()):
    PLUGIN = 25

    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)

        addLevelName(self.PLUGIN, "PLUGIN")

    def plugin(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.PLUGIN):
            self._log(self.PLUGIN, msg, args, **kwargs)
