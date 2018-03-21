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

    def run(self, *sys_args, **kwargs):
        if sys_args[0].config:
            app.start(sys_args[0].config)
        else:
            app.start()
