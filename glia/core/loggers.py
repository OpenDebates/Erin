import logging
from logging import NOTSET, addLevelName, getLoggerClass

discord_logger = logging.getLogger('discord')
discord_handler = logging.StreamHandler()
discord_logger.setLevel(logging.INFO)
discord_formatter = logging.Formatter(
    '%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
    datefmt="[%Y-%m-%d %H:%M:%S %z]"
)
discord_handler.setFormatter(discord_formatter)
discord_logger.addHandler(discord_handler)


# Don't forget to call logging.setLoggerClass(BotLogger) at the start
# of the code to ensure that this formatting is used everywhere.
# The current logger class is set in glia.__init__.py.
class BotLogger(getLoggerClass()):
    DATABASE = 15
    COMMAND = 16
    PLUGIN = 17

    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)

        addLevelName(self.DATABASE, "DATABASE")
        addLevelName(self.COMMAND, "COMMAND")
        addLevelName(self.PLUGIN, "PLUGIN")

    def database(self, msg, *args, **kwargs):
        """
        Call to log database operations from within plugins.
        """
        if self.isEnabledFor(self.DATABASE):
            self._log(self.DATABASE, msg, args, **kwargs)

    def command(self, msg, *args, **kwargs):
        """
        Logs commands that are sent to the bot by users.
        """
        if self.isEnabledFor(self.COMMAND):
            self._log(self.COMMAND, msg, args, **kwargs)

    def plugin(self, msg, *args, **kwargs):
        """
        Plugin specific logs to let users know something happened.
        """
        if self.isEnabledFor(self.PLUGIN):
            self._log(self.PLUGIN, msg, args, **kwargs)
