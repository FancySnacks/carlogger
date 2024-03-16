"""Argument parser for CLI input"""

import argparse

from abc import abstractmethod, ABC


class ArgParser:
    """Handles console arguments and executes related functions."""
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="Car Logger",
                                              usage="carlogger [-args]",
                                              description="description",
                                              epilog="epilog",
                                              formatter_class=argparse.RawDescriptionHelpFormatter)
        self.subparsers = self.parser.add_subparsers(help="Subcommands")

        self.subparser_obj: list[Subparser] = []

        self.parsed_args: dict = {}

    def setup_args(self):
        # --gui argument
        # argument for creating collections
        # argument for creating components
        # argument for creating entries

        # ==== Returning Values ==== #

        self.parser.add_argument('--gui',
                                 action='store_true',
                                 help="Open graphical user interface for the app.")

    def add_subparser(self, subparser):
        self.subparser_obj.append(subparser)
        subparser.create_subparser()

    def parse_args(self, args: list[str]) -> dict:
        self.parsed_args = self.parser.parse_args(args).__dict__
        return self.parsed_args

    def get_subparser_type(self, argv: list[str]) -> str:
        if 'add' in argv:
            return 'add'

        if 'read' in argv:
            return 'read'


class Subparser(ABC):
    @abstractmethod
    def __init__(self, parser_parent: ArgParser):
        self.parser_parent = parser_parent

    @abstractmethod
    def create_subparser(self):
        pass


class ReadSubparser(Subparser):
    def __init__(self, parser_parent: ArgParser):
        self.parser_parent = parser_parent

    def create_subparser(self):
        self.return_parser = self.parser_parent.subparsers.add_parser('read',
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
                                        metavar='filter options',
                                        required=False)


class AddSubparser(Subparser):
    def __init__(self, parser_parent: ArgParser):
        self.parser_parent = parser_parent

    def create_subparser(self):
        self.add_parser = self.parser_parent.subparsers.add_parser('add',
                                                                   help="Add new car, collection, component or log entry.",
                                                                   formatter_class=argparse.RawTextHelpFormatter)

        self.add_subparsers = self.add_parser.add_subparsers(help="Subcommands")

        # ===== Add Car ===== #

        self.add_car_parser = self.add_subparsers.add_parser('car')


        self.add_car_parser.add_argument('--name',
                                         type=str,
                                         required=True)

        self.add_car_parser.add_argument('--manufacturer',
                                         type=str,
                                         required=True)

        self.add_car_parser.add_argument('--model',
                                         type=str,
                                         required=True)

        self.add_car_parser.add_argument('--year',
                                         type=int,
                                         required=True)

        self.add_car_parser.add_argument('--mileage',
                                         type=int,
                                         required=True)

        self.add_car_parser.add_argument('--body',
                                         type=str,
                                         required=True)

        self.add_car_parser.add_argument('--length',
                                         type=int,
                                         required=True)

        self.add_car_parser.add_argument('--weight',
                                         type=int,
                                         required=True)

        # ===== Add Collection ===== #

        self.add_collection_parser = self.add_subparsers.add_parser('collection')

        self.add_collection_parser.add_argument('--name',
                                                type=str,
                                                required=True)

        self.add_collection_parser.add_argument('--car',
                                                type=str,
                                                required=True)

        # ===== Add Component ===== #

        self.add_component_parser = self.add_subparsers.add_parser('component')

        self.add_component_parser.add_argument('--name',
                                               type=str,
                                               required=True)

        self.add_component_parser.add_argument('--car',
                                               type=str,
                                               required=True)

        self.add_component_parser.add_argument('--collection',
                                               type=str,
                                               required=True)
