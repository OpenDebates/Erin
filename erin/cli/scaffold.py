from cookiecutter.main import cookiecutter

from erin.cli import CommandFactory


class ScaffoldCommand(CommandFactory):
    def __init__(self, parser, *args, **kwargs):
        self.parser = parser.add_parser(*args, **kwargs)
        self.parser.set_defaults(action=self.run)

    def run(self, *sys_args, **kwargs):
        cookiecutter("https://github.com/DiscordFederation/cookiecutter-erin.git")
