import argparse
import logging
import sys

from verboselogs import VerboseLogger

import erin
from erin.cli.scaffold import ScaffoldCommand
from erin.cli.start import StartCommand

# Constants
LOG_FORMAT = "%(asctime)s %(name)-18s %(levelname)-8s %(message)s"
DATE_FORMAT = "[%Y-%m-%d %H:%M:%S %z]"

# Set Library Logging Formats
logging.setLoggerClass(VerboseLogger)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
root_logger = logging.getLogger(__name__)
root_logger.addHandler(stream_handler)


def _optional_commands(parser):
    """
    Optional cli passed directly to the main parser.
    """
    parser.add_argument(
        "-V", "--version",
        version=f"%(prog)s {erin.__version__}",
        action="version"
    )
    parser.add_argument(
        "-v", "--verbose",
        help="increase output verbosity",
        action="store_true"
    )
    return parser


def _main_commands(parser):
    """
    Commands for the cli subparser is defined in
    :mod:`erin.cli` and called here.

    You can pass any of the arguments except `action` to these cli
    as defined by :func:`argparse.ArgumentParser.add_parser`.
    """
    StartCommand(
        parser,
        "start",
        aliases=["run"],
        help="start the server"
    )
    ScaffoldCommand(
        parser,
        "scaffold",
        aliases=["init"],
        help="create new erin project"
    )
    return parser


def main(args=None):
    """The main entry point."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Fully Fledged Discord Bot Framework"
    )

    parser = _optional_commands(parser)
    parser_commands = parser.add_subparsers(
        title="Commands",
        dest="cli"
    )
    parser_commands = _main_commands(parser_commands)

    if isinstance(args, list):
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    if args.verbose:

        # This is different from logging output verbosity. Enabling this
        # will print command internals directly to STDOUT regardless of
        # the settings defined in the logging module. Only recommended
        # for use by developers.
        print("Verbose Mode: Enabled")

    try:
        args.action(args)
    except AttributeError:
        pass

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit(0)


if __name__ == "__main__":
    main()
