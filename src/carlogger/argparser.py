"""Argument parser for CLI input"""

import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="Car Logger",
                                              usage="carlogger [-args]",
                                              description="description",
                                              epilog="epilog",
                                              formatter_class=argparse.RawDescriptionHelpFormatter)
        self.subparsers = self.parser.add_subparsers(help="Subcommands")

    def setup_args(self):
        # --gui argument
        # argument for creating collections
        # argument for creating components
        # argument for creating entries

        # ==== Returning Values ==== #

        self.return_parser = self.subparsers.add_parser('read',
                                                        help="Return car info, collection/component list  or log entries.")
        self.return_parser.add_argument('--car',
                                        type=str,
                                        help="Return car info via name.",
                                        required=True)

        self.return_parser.add_argument('--collection',
                                        type=str,
                                        help="Return collection via name.",
                                        nargs='*',
                                        required=False)

        self.return_parser.add_argument('--component',
                                        type=str,
                                        help="Return component via name.",
                                        nargs='*',
                                        required=False)

        self.return_parser.add_argument('--entry',
                                        type=str,
                                        help="Return entry via name.",
                                        nargs='*',
                                        required=False)

        # ==== Creating Objects and Entries ==== #

        self.add_parser = self.subparsers.add_parser('add',
                                                     help="Add new car, collection, component or log entry.")

    def parse_args(self, args: list[str]) -> dict:
        return self.parser.parse_args(args).__dict__
