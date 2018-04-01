import sys
from logging import getLoggerClass, NOTSET, addLevelName


class BotLogger(getLoggerClass()):
    PLUGIN = 25
    COMMAND = 24

    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)

        addLevelName(self.PLUGIN, "PLUGIN")
        addLevelName(self.COMMAND, "COMMAND")

    def plugin(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.PLUGIN):
            self._log(self.PLUGIN, msg, args, **kwargs)

    def command(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.COMMAND):
            self._log(self.COMMAND, msg, args, **kwargs)


SANIC_LOGGER_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,

    loggers={
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error"
        },

        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access"
        },
        "discord": {
            "level": "INFO",
            "handlers": ["console"]
        }
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout
        },
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: " +
                      "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
    }
)
