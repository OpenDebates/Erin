from logging import getLoggerClass, NOTSET, addLevelName, setLoggerClass

LEVEL_STYLES = {
    'debug': {'color': 'green'},
    'info': {},
    'plugin': {'color': 'blue'},
    'command': {'color': 'blue'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'color': 'red', 'bold': True}
}

PLUGIN = 25
COMMAND = 24


class EnigmaLogger(getLoggerClass()):
    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)

        addLevelName(PLUGIN, "PLUGIN")
        addLevelName(COMMAND, "COMMAND")

    def plugin(self, msg, *args, **kwargs):
        if self.isEnabledFor(PLUGIN):
            self._log(PLUGIN, msg, args, **kwargs)

    def command(self, msg, *args, **kwargs):
        if self.isEnabledFor(COMMAND):
            self._log(COMMAND, msg, args, **kwargs)


setLoggerClass(EnigmaLogger)
