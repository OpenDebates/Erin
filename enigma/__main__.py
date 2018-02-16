import argparse
import sys


def _optional_commands(parser):
    parser.add_argument(
            "-V", "--version",
            version="%(prog)s {}".format(enigma.__version__),
            action="version"
        )
    parser.add_argument(
        "-v", "--verbose",
        help="increase output verbosity",
        action="store_true"
    )
    return parser


def _main_commands(parser):
    # Any important commands we need go here.
    return parser


def main(args=None):
    """The main entry point."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="The Polyglot Discord Bot"
    )

    parser = _optional_commands(parser)
    parser_commands = parser.add_subparsers(
        title="Commands",
        dest="commands"
    )
    parser_commands = _main_commands(parser_commands)

    if type(args) == list:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    try:
        args.action(args)  # Investigate why this fails
    except AttributeError:
        pass

    if len(sys.argv[1:]) == 0:
        pass  # This is where we start running code

    if args.verbose:
        print("Verbosity enabled!")


if __name__ == "__main__":
    main()
