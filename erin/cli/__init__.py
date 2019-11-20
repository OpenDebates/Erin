from abc import ABCMeta, abstractmethod


class CommandFactory(object):
    """
    Makes building commands for cli easier. Why not :class:`argparse.Action`?
    We tried doing that, but Action can't handle subparsers that have
    actions that need it's own extra sub cli. Plus this way, we
    have a neat structure for cli.

    When defining new sub commands, just pass your command's method
    name to the action key.

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Kittens will die if this isn't implemented.
        """
        raise NotImplementedError(f"This method is not optional")


if __name__ == "__main__":
    pass
