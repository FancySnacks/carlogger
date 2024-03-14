"""Argument parser for CLI input"""

import argparse


class ArgParser:
    """Handles console arguments and executes related functions."""
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

        self.parser.add_argument('--gui',
                                 action='store_true',
                                 help="Open graphical user interface for the app.")


        self.return_parser = self.subparsers.add_parser('read',
                                                        help="Return car info, collection/component list  or "
                                                             "log entries.",
                                                        formatter_class=argparse.RawTextHelpFormatter)
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
                                        help="Return entry via name.\n"
                                             "Accepts multiple string arguments as filters:\n"
                                             "By default if no arg is present shows all entries in a given relation\n"
                                             "'*' - (default) shows all entries\n"
                                             "'entry id' - return entry of this id, trumps all other filters\n"
                                             "'category' - returns entries of this category"
                                             "['check', 'part swap', 'repair', 'fluid change', 'fluid_add', 'other']\n"
                                             "'<mileage' - return entries assigned to a lesser mileage\n"
                                             "'>mileage' - return entries assigned to a greater mileage\n"
                                             "'DD-MM-YYYY' - show entries made on specific date\n"
                                             "'<DD-MM-YYYY' - show entries younger than specified date\n"
                                             "'>DD-MM-YYYY' - show entries older than specified date\n"
                                             "'DD-MM-YYYY-DD-MM-YYYY' - show entries created in this date range\n"
                                             "'[-]n' - show 'n' amount of entries from youngest to oldest, '-' "
                                             "before integer will show oldest to youngest instead\n",
                                        nargs='*',
                                        default=['*'],
                                        metavar='filter options',
                                        required=False)

        # ==== Creating Objects and Entries ==== #

        self.add_parser = self.subparsers.add_parser('add',
                                                     help="Add new car, collection, component or log entry.")

    def parse_args(self, args: list[str]) -> dict:
        return self.parser.parse_args(args).__dict__
