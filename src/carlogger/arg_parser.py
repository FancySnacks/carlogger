"""Argument parser for CLI input"""

import argparse

from datetime import datetime
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
        self.parser.add_argument('--gui',
                                 action='store_true',
                                 help="Open graphical user interface for the app.")

        self.add_subparser(AddSubparser(self))
        self.add_subparser(ReadSubparser(self))
        self.add_subparser(DeleteSubparser(self))

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

        if 'delete' in argv:
            return 'delete'


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
                                                                           "log entries by specifying the car.\n",
                                                                      formatter_class=argparse.RawTextHelpFormatter)
        self.return_parser.add_argument('--car',
                                        type=str,
                                        metavar="CAR_NAME",
                                        help="Return car info via name.",
                                        required=True)

        self.return_parser.add_argument('--collection',
                                        type=str,
                                        metavar="COLLECTION_NAME",
                                        help="Return collection via name.",
                                        nargs='*',
                                        required=False)

        self.return_parser.add_argument('--component',
                                        type=str,
                                        metavar="COMPONENT_NAME",
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
                                        metavar='FILTER_OPTIONS',
                                        required=False)


class AddSubparser(Subparser):
    def __init__(self, parser_parent: ArgParser):
        self.parser_parent = parser_parent

    def create_subparser(self):
        self.add_parser = self.parser_parent.subparsers.add_parser('add',
                                                                   help="Add new car, collection, component or log entry.",
                                                                   formatter_class=argparse.RawTextHelpFormatter)

        self.add_subparsers = self.add_parser.add_subparsers(help="Choose item type to add.\n"
                                                                  "Collections and components require only names and"
                                                                  "parenting car and/or collection.\n"
                                                                  "Cars and entries require much more data.")

        # ===== Add Car ===== #

        self.add_car_parser = self.add_subparsers.add_parser('car')

        self.add_car_parser.add_argument('--name',
                                         type=str,
                                         help="User-defined car name for easy access.",
                                         required=True)

        self.add_car_parser.add_argument('--manufacturer',
                                         type=str,
                                         required=True)

        self.add_car_parser.add_argument('--model',
                                         type=str,
                                         required=True)

        self.add_car_parser.add_argument('--year',
                                         type=int,
                                         help="Year of make.",
                                         required=True)

        self.add_car_parser.add_argument('--mileage',
                                         type=int,
                                         required=True)

        self.add_car_parser.add_argument('--body',
                                         type=str,
                                         help="Hatchback, sedan, coupe, station wagon, SUV etc.",
                                         required=True)

        self.add_car_parser.add_argument('--length',
                                         type=int,
                                         required=True)

        self.add_car_parser.add_argument('--weight',
                                         type=int,
                                         required=True)

        self.add_car_parser.add_argument('-p',
                                         type=str,
                                         help='More car properties as defined by the user, stored into a list.',
                                         metavar='OTHER CAR PROPERTIES',
                                         nargs='*',
                                         default=[])

        # ===== Add Collection ===== #

        self.add_collection_parser = self.add_subparsers.add_parser('collection')

        self.add_collection_parser.add_argument('-n',
                                                '--name',
                                                metavar="COLLECTION NAME",
                                                type=str,
                                                required=True)

        self.add_collection_parser.add_argument('--car',
                                                type=str,
                                                help="Parent car.",
                                                required=True)

        # ===== Add Component ===== #

        self.add_component_parser = self.add_subparsers.add_parser('component')

        self.add_component_parser.add_argument('-n',
                                               '--name',
                                               metavar="COMPONENT NAME",
                                               type=str,
                                               required=True)

        self.add_component_parser.add_argument('--car',
                                               type=str,
                                               help="Parent car.",
                                               required=True)

        self.add_component_parser.add_argument('--collection',
                                               help="Parent collection.",
                                               type=str,
                                               required=True)

        # ===== Add Entry ===== #

        self.add_entry_parser = self.add_subparsers.add_parser('entry')

        self.add_entry_parser.add_argument('--car',
                                           help="Parent collection.",
                                           type=str,
                                           required=True)

        self.add_entry_parser.add_argument('--collection',
                                           help="Parent collection.",
                                           type=str,
                                           required=True)

        self.add_entry_parser.add_argument('--component',
                                           type=str,
                                           required=True)

        self.add_entry_parser.add_argument('--desc',
                                           help='Short entry description.',
                                           type=str,
                                           required=True)

        self.add_entry_parser.add_argument('--date',
                                           type=str,
                                           help="FORMAT: 'DD-MM-YY'.\n"
                                                "By default - current day.\n",
                                           default=datetime.today().date().strftime("%d-%m-%Y"))

        self.add_entry_parser.add_argument('--mileage',
                                           type=int,
                                           required=True)

        self.add_entry_parser.add_argument('--category',
                                           type=str,
                                           choices=['check', 'swap', 'repair', 'fluid_change', 'fluid_add', 'other'],
                                           required=True)

        self.add_entry_parser.add_argument('--tags',
                                           type=str,
                                           help="Custom tags used for easier search and filtering.",
                                           nargs='*',
                                           default=[])


class DeleteSubparser(Subparser):
    def __init__(self, parser_parent: ArgParser):
        self.parser_parent = parser_parent

    def create_subparser(self):
        self.delete_parser = self.parser_parent.subparsers.add_parser('delete',
                                                                      help="Delete specified car, collection, component or log entry.",
                                                                      formatter_class=argparse.RawTextHelpFormatter)

        self.delete_subparsers = self.delete_parser.add_subparsers(help="Choose which item to delete, "
                                                                        "then enter name or unique ID.\n"
                                                                        "For entries only ID is necessary.\n"
                                                                        "Collections and components removals need to be"
                                                                        " specific, you have to add parenting car or "
                                                                        "collection.")

        # ===== Delete Car ===== #

        self.delete_car_parser = self.delete_subparsers.add_parser('car')

        self.delete_car_parser.add_argument('-n',
                                            '--name',
                                            type=str,
                                            required=True)

        self.delete_car_parser.add_argument('-f',
                                            '--forced',
                                            help="Delete item and it's children even if it's not empty.\n",
                                            action='store_true')

        # ===== Delete Collection ===== #

        self.delete_collection_parser = self.delete_subparsers.add_parser('collection')

        self.delete_collection_parser.add_argument('-n',
                                                   '--name',
                                                   type=str,
                                                   required=True)

        self.delete_collection_parser.add_argument('--car',
                                                   type=str,
                                                   required=True)

        self.delete_collection_parser.add_argument('-f',
                                                   '--forced',
                                                   help="Delete item and it's children even if it's not empty.\n",
                                                   action='store_true')

        # ===== Delete Component ===== #

        self.delete_component_parser = self.delete_subparsers.add_parser('component')

        self.delete_component_parser.add_argument('-n',
                                                  '--name',
                                                  type=str,
                                                  required=True)

        self.delete_component_parser.add_argument('--car',
                                                  type=str,
                                                  required=True)

        self.delete_component_parser.add_argument('--collection',
                                                  type=str,
                                                  required=True)

        self.delete_component_parser.add_argument('-f',
                                                  '--forced',
                                                  help="Delete item and it's children even if it's not empty.\n",
                                                  action='store_true')

        # ===== Delete Entry ===== #

        self.delete_entry_parser = self.delete_subparsers.add_parser('entry')

        self.delete_entry_parser.add_argument('-id',
                                              '--id',
                                              type=str,
                                              required=True)

        self.delete_entry_parser.add_argument('--car',
                                              type=str,
                                              required=True)
