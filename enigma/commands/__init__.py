from abc import ABCMeta, abstractmethod


class CommandFactory(object):
    """
    Makes building commands easier. Why not :class:`argparse.Action`?
    We tried doing that, but Action can't handle subparsers that have
    actions that need it's own extra sub commands. Plus this way, we
    have a neat structure for commands.

    When defining new sub commands, just pass your command's method
    name to the action key.

    """
    __metaclass__ = ABCMeta

    def __init__(self, parser, *args, **kwargs):
        self.parser = parser.add_parser(*args, **kwargs)
        self.parser.set_defaults(action=self.run)

    @abstractmethod
    def run(self, args):
        """
        Kittens will die if this isn't implemented.
        """
        raise NotImplementedError(
            f"This method is not optional"
        )


if __name__ == "__main__":
    pass
