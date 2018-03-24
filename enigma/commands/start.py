import argparse

from enigma import app
from enigma.commands import CommandFactory


class StartCommand(CommandFactory):
    def __init__(self, parser, *args, **kwargs):
        self.parser = parser.add_parser(*args, **kwargs)
        self.parser.set_defaults(action=self.run)

        # Config File
        self.parser.add_argument(
            '--config',
            type=argparse.FileType('r')
        )

        # Set Logging Levels
        self.choices = [
            'debug', 'info', 'plugin', 'command', 'warning', 'error',
            'critical'
        ]
        self.parser.add_argument(
            '--log',
            choices=self.choices,
            type=str.lower
        )

    def run(self, *sys_args, **kwargs):
        passed_args = {
            'config_file': None,
            'log_level': None
        }
        if sys_args[0].config:
            passed_args['config_file'] = sys_args[0].config
        if sys_args[0].log:
            passed_args['log_level'] = sys_args[0].log

        app.start(**passed_args)
