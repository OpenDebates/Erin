from enigma.commands import CommandFactory

from enigma import app


class StartCommand(CommandFactory):
    def run(self, args):
        app.start()
