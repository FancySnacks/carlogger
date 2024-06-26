"""Subparsers for add, read and delete functionality."""

import argparse

from abc import ABC, abstractmethod

from carlogger.const import TODAY


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split("=")
            getattr(namespace, self.dest)[key] = self.clamp_value(value)

    def clamp_value(self, value) -> ...:
        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False

        try:
            return int(value)
        except ValueError:
            return value


class Subparser(ABC):
    @abstractmethod
    def __init__(self, parser_parent):
        self.parser_parent = parser_parent

    @abstractmethod
    def create_subparser(self):
        pass


class ReadSubparser(Subparser):
    def __init__(self, parser_parent):
        self.parser_parent = parser_parent

    def add_sort_parser(self):
        for sp_name, sp_obj in self.read_subparsers.choices.items():
            sp_obj.add_argument('--sort', help='Sort returned items by a specific key.')
            sp_obj.add_argument('--reverse', action='store_true',
                                help="Sort returned items in reversed way, does nothing without '--sort' flag.")

    def create_subparser(self):
        self.read_parser = self.parser_parent.subparsers.add_parser('read',
                                                                    help="Return car info, collection/component list"
                                                                         " or log entries by specifying the car.\n",
                                                                    formatter_class=argparse.RawTextHelpFormatter)

        self.read_subparsers = self.read_parser.add_subparsers(help="Choose item type to read.\n")

        # ===== READ CAR ===== #

        self.read_car_parser = self.read_subparsers.add_parser('car')

        self.read_car_parser.add_argument('name',
                                          type=str,
                                          metavar="CAR_NAME",
                                          help="Return car info via name."
                                               "'*' (default) - returns all cars in a save directory.",
                                          default='*')

        # ===== READ COLLECTION ===== #

        self.read_collection_parser = self.read_subparsers.add_parser('collection')

        self.read_collection_parser.add_argument('name',
                                          type=str,
                                          metavar="COLLECTION_NAME",
                                          help="Return collection via name."
                                               "'*' (default) - returns all collections belonging to specified car.",
                                          default='*')

        self.read_collection_parser.add_argument('--car',
                                                 type=str,
                                                 metavar="CAR_NAME",
                                                 help="Parent car name.",
                                                 required=True)

        # ===== READ COMPONENT ===== #

        self.read_component_parser = self.read_subparsers.add_parser('component')

        self.read_component_parser.add_argument('name',
                                          type=str,
                                          metavar="COMPONENT_NAME",
                                          help="Return component via name."
                                               "'*' (default) - returns all components belonging to specified car.",
                                          default='*')

        self.read_component_parser.add_argument('--car',
                                                type=str,
                                                metavar="CAR_NAME",
                                                help="Parent car name.",
                                                required=True)

        # ===== READ ENTRY ===== #

        self.read_entry_parser = self.read_subparsers.add_parser('entry')

        self.read_entry_parser.add_argument('data',
                                            type=str,
                                            help="Return entry via name.\n"
                                                 "Accepts multiple string arguments as filters:\n"
                                                 "By default if no arg is present shows all entries in "
                                                 "a given relation\n"
                                                 "'*' - (default) shows all entries\n"
                                                 "'entry id' - return entry of this id, trumps all other filters\n"
                                                 "'category' - returns entries of this category"
                                                 "['check', 'part swap', 'repair', 'fluid change', '"
                                                 "fluid_add', 'other']\n"
                                                 "'<mileage' - return entries assigned to a lesser mileage\n"
                                                 "'>mileage' - return entries assigned to a greater mileage\n"
                                                 "'mileage-mileage' - show entries created in this mileage range\n"
                                                 "'DD-MM-YYYY' - show entries made on specific date\n"
                                                 "'<DD-MM-YYYY' - show entries younger than specified date\n"
                                                 "'>DD-MM-YYYY' - show entries older than specified date\n"
                                                 "'DD-MM-YYYY-DD-MM-YYYY' - show entries created in this "
                                                 "date range (inclusive)\n"
                                                 "'[-]n' - show 'n' amount of entries from youngest to oldest, '-' "
                                                 "before integer will show oldest to youngest instead\n",
                                            nargs='*',
                                            metavar='FILTER_OPTIONS',
                                            default='*')

        self.read_entry_parser.add_argument('--car',
                                            type=str,
                                            metavar="CAR_NAME",
                                            help="Parent car name.",
                                            required=True)

        self.add_sort_parser()


class AddSubparser(Subparser):
    def __init__(self, parser_parent):
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

        self.add_car_parser.add_argument('--custom',
                                         action=ParseKwargs, type=str,
                                         help="More car properties as defined by the user, "
                                              "stored into a dictionary.\n"
                                              "Pass arguments as 'key=value' pairs, separated by spaces.\n"
                                              "Example: --custom 'key=val' 'key2=value2'",
                                         metavar='OTHER CAR PROPERTIES',
                                         dest='custom_info',
                                         nargs='*',
                                         default={})

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

        self.add_collection_parser.add_argument('--parent',
                                                type=str,
                                                metavar="PARENT COLLECTION NAME",
                                                help="Parent collection.")

        self.add_collection_parser.add_argument('--custom',
                                                action=ParseKwargs,
                                                type=str,
                                                help="More collection properties as defined by the user, "
                                                     "stored into a dictionary.\n"
                                                     "Pass arguments as 'key=value' pairs, separated by spaces.\n"
                                                     "Example: --custom 'key=val' 'key2=value2'",
                                                metavar='CUSTOM ENTRY PROPERTIES',
                                                dest='custom_info',
                                                nargs='*',
                                                default={})

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

        self.add_component_parser.add_argument('--custom',
                                               action=ParseKwargs,
                                               type=str,
                                               help="More component properties as defined by the user, "
                                                    "stored into a dictionary.\n"
                                                    "Pass arguments as 'key=value' pairs, separated by spaces.\n"
                                                    "Example: --custom 'key=val' 'key2=value2'",
                                               metavar='CUSTOM ENTRY PROPERTIES',
                                               dest='custom_info',
                                               nargs='*',
                                               default={})

        # ===== Add Entry ===== #

        self.add_entry_parser = self.add_subparsers.add_parser('entry')

        self.add_entry_parser.add_argument('--car',
                                           help="Parent car.",
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
                                           default=TODAY)

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

        self.add_entry_parser.add_argument('--custom',
                                           action=ParseKwargs,
                                           type=str,
                                           help="More entry properties as defined by the user, "
                                                "stored into a dictionary.\n"
                                                "Pass arguments as 'key=value' pairs, separated by spaces.\n"
                                                "Example: --custom 'catalogue_number=450159' 'warranty=5 years'",
                                           metavar='CUSTOM ENTRY PROPERTIES',
                                           dest='custom_info',
                                           nargs='*',
                                           default={})

        # ===== Add Scheduled Entry ===== #

        self.add_scheduled_entry_parser = self.add_subparsers.add_parser('scheduled_entry')

        self.add_scheduled_entry_parser.add_argument('--car',
                                                     help="Parent car.",
                                                     type=str,
                                                     required=True)

        self.add_scheduled_entry_parser.add_argument('--collection',
                                                     help="Parent collection.",
                                                     type=str,
                                                     required=True)

        self.add_scheduled_entry_parser.add_argument('--component',
                                                     type=str,
                                                     required=True)

        self.add_scheduled_entry_parser.add_argument('--desc',
                                                     help='Short entry description.',
                                                     type=str,
                                                     required=True)

        self.add_scheduled_entry_parser.add_argument('--date',
                                                     type=str,
                                                     help="FORMAT: 'DD-MM-YY'.\n"
                                                          "If passed, frequency will be ignored and entry will "
                                                          "be non-repeating.\n"
                                                          "Empty by default.\n",
                                                     default="")

        self.add_scheduled_entry_parser.add_argument('--mileage',
                                                     type=int,
                                                     required=True)

        self.add_scheduled_entry_parser.add_argument('--category',
                                                     type=str,
                                                     choices=['check', 'swap', 'repair', 'fluid_change', 'fluid_add',
                                                              'other'],
                                                     required=True)

        self.add_scheduled_entry_parser.add_argument('--tags',
                                                     type=str,
                                                     help="Custom tags used for easier search and filtering.",
                                                     nargs='*',
                                                     default=[])

        self.add_scheduled_entry_parser.add_argument('--rule',
                                                     type=str,
                                                     choices=['date', 'mileage'],
                                                     default='date',
                                                     required=True)

        self.add_scheduled_entry_parser.add_argument('--frequency',
                                                     type=int,
                                                     help="Number of days / mileage between each Scheduled Entry "
                                                          "if it's repeating (if '--repeating' argument is passed).\n"
                                                          "'1' by default.",
                                                     default=1)

        self.add_scheduled_entry_parser.add_argument('--repeating',
                                                     action='store_true',
                                                     help="Presence of this argument will set scheduled entry to be "
                                                          "repeated each time it is marked as done.\n"
                                                          "Number of days/mileage between each loop is defined by "
                                                          "'--frequency' argument.\n")

        self.add_scheduled_entry_parser.add_argument('--custom',
                                                     action=ParseKwargs,
                                                     type=str,
                                                     help="More entry properties as defined by the user, "
                                                          "stored into a dictionary.\n"
                                                          "Pass arguments as 'key=value' pairs, separated by spaces.\n"
                                                          "Example: --custom 'catalogue_number=450159' 'warranty=5 years'",
                                                     metavar='CUSTOM ENTRY PROPERTIES',
                                                     dest='custom_info',
                                                     nargs='*',
                                                     default=[])


class DeleteSubparser(Subparser):
    def __init__(self, parser_parent):
        self.parser_parent = parser_parent

    def add_clear_parser(self):
        for sp_name, sp_obj in list(self.delete_subparsers.choices.items())[:-1:]:
            sp_obj.add_argument('--clear', action='store_true',
                                help="Clear children inside of specified item, instead of deleting the item itself.")

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
                                            metavar="CAR_NAME",
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
                                                   metavar="COLLECTION_NAME",
                                                   type=str,
                                                   required=True)

        self.delete_collection_parser.add_argument('--car',
                                                   metavar="CAR_NAME",
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
                                                  metavar="COMPONENT_NAME",
                                                  type=str,
                                                  required=True)

        self.delete_component_parser.add_argument('--car',
                                                  metavar="CAR_NAME",
                                                  type=str,
                                                  required=True)

        self.delete_component_parser.add_argument('--collection',
                                                  metavar="COLLECTION_NAME",
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
                                              metavar="ID/INDEX",
                                              help="Pass unique entry ID or it's index number in a component.\n"
                                                   "When deleting via index it's mandatory to specify parent component.",
                                              type=str,
                                              required=True)

        self.delete_entry_parser.add_argument('--car',
                                              metavar="CAR_NAME",
                                              type=str,
                                              required=True)

        self.delete_entry_parser.add_argument('--component',
                                              metavar="COMPONENT_NAME",
                                              help="Not mandatory, only used when deleting entry by index number.",
                                              type=str)

        self.add_clear_parser()


class UpdateSubparser(Subparser):
    def __init__(self, parser_parent):
        self.parser_parent = parser_parent

    def create_subparser(self):
        self.update_parser = self.parser_parent.subparsers.add_parser('update',
                                                                      help="Update data of car, collection, "
                                                                           "component or entry.",
                                                                      formatter_class=argparse.RawTextHelpFormatter)

        self.update_subparsers = self.update_parser.add_subparsers(help="Choose item type to update.\n")

        # ===== UPDATE CAR ===== #

        self.update_car_parser = self.update_subparsers.add_parser('car')

        self.update_car_parser.add_argument('-c',
                                            '--car',
                                            type=str,
                                            metavar="CAR_NAME",
                                            help="Update specified car by name.",
                                            required=True)

        self.update_car_parser.add_argument('--name',
                                            type=str,
                                            help="Update car name.")

        self.update_car_parser.add_argument('--manufacturer',
                                            type=str)

        self.update_car_parser.add_argument('--model',
                                            type=str)

        self.update_car_parser.add_argument('--year',
                                            type=int)

        self.update_car_parser.add_argument('--mileage',
                                            type=int)

        self.update_car_parser.add_argument('--body',
                                            type=str,
                                            help="Hatchback, sedan, coupe, station wagon, SUV etc.")

        self.update_car_parser.add_argument('--length',
                                            type=int)

        self.update_car_parser.add_argument('--weight',
                                            type=int)

        self.update_car_parser.add_argument('-p',
                                            type=str,
                                            help='More car properties as defined by the user, stored into a list.',
                                            metavar='OTHER CAR PROPERTIES',
                                            nargs='*',
                                            default=[])

        self.update_car_parser.add_argument('--custom',
                                            action=ParseKwargs, type=str,
                                            help="More entry properties as defined by the user, "
                                                 "stored into a dictionary.\n"
                                                 "Pass arguments as 'key=value' pairs, separated by spaces.\n"
                                                 "Example: --custom 'catalogue_number=450159' 'warranty=5 years'",
                                            metavar='OTHER CAR PROPERTIES',
                                            dest='custom_info',
                                            nargs='*',
                                            default=[])

        # ===== UPDATE COLLECTION ===== #

        self.update_collection_parser = self.update_subparsers.add_parser('collection')

        self.update_collection_parser.add_argument('-c',
                                                   '--collection',
                                                   metavar="COLLECTION NAME",
                                                   help="Update collection via name.",
                                                   type=str,
                                                   required=True)

        self.update_collection_parser.add_argument('--car',
                                                   type=str,
                                                   metavar="CAR_NAME",
                                                   help="Parent car name.",
                                                   required=True)

        self.update_collection_parser.add_argument('--name',
                                                   help='Update collection name.',
                                                   type=str)

        # ===== UPDATE COMPONENT ===== #

        self.update_component_parser = self.update_subparsers.add_parser('component')

        self.update_component_parser.add_argument('-c',
                                                  '--component',
                                                  type=str,
                                                  metavar="COMPONENT_NAME",
                                                  help="Update component via name.",
                                                  required=True)

        self.update_component_parser.add_argument('--car',
                                                  type=str,
                                                  metavar="CAR_NAME",
                                                  help="Parent car name.",
                                                  required=True)

        self.update_component_parser.add_argument('--name',
                                                  help='Update component name.',
                                                  type=str)

        # ===== UPDATE ENTRY ===== #

        self.update_entry_parser = self.update_subparsers.add_parser('entry')

        self.update_entry_parser.add_argument('-id',
                                              '--id',
                                              metavar="ID",
                                              help="Unique entry ID.\n",
                                              type=str,
                                              required=True)

        self.update_entry_parser.add_argument('--car',
                                              help="Parent car.",
                                              type=str,
                                              required=True)

        self.update_entry_parser.add_argument('--desc',
                                              help='Short entry description.',
                                              type=str)

        self.update_entry_parser.add_argument('--date',
                                              type=str,
                                              help="FORMAT: 'DD-MM-YY'.\n")

        self.update_entry_parser.add_argument('--mileage',
                                              type=int)

        self.update_entry_parser.add_argument('--category',
                                              type=str,
                                              choices=['check', 'swap', 'repair', 'fluid_change', 'fluid_add', 'other'])

        self.update_entry_parser.add_argument('--tags',
                                              type=str,
                                              help="Custom tags used for easier search and filtering.",
                                              nargs='*',
                                              default=[])

        self.update_entry_parser.add_argument('--complete',
                                              help="Scheduled Log Entries only: use to set log as complete and add to "
                                                   "history. If entry is repeating it will be renewed and scheduled.",
                                              action='store_true',
                                              default=False)

        self.update_entry_parser.add_argument('--custom',
                                              action=ParseKwargs, type=str,
                                              help="More entry properties as defined by the user, "
                                                   "stored into a dictionary.\n"
                                                   "Pass arguments as 'key=value' pairs, separated by spaces.\n"
                                                   "Example: --custom 'catalogue_number=450159' 'warranty=5 years'",
                                              metavar='OTHER CAR PROPERTIES',
                                              dest='custom_info',
                                              nargs='*',
                                              default=[])


class ImportSubparser(Subparser):
    def __init__(self, parser_parent):
        self.parser_parent = parser_parent

    def add_path_arg(self):
        for sp_name, sp_obj in list(self.import_parsers.choices.items()):
            sp_obj.add_argument('path',
                                metavar="FILEPATH",
                                help="System path leading to file that you want to import. "
                                     "Valid formats: [.json, .txt, .csv]",
                                type=str)

    def add_nochild_arg(self):
        for sp_name, sp_obj in list(self.import_parsers.choices.items())[1:]:
            sp_obj.add_argument('--nochildren',
                                help="Import item without child elements.",
                                action='store_true')

    def create_subparser(self):
        self.import_parser = self.parser_parent.subparsers.add_parser('import',
                                                                      help="Import file and save as new item.",
                                                                      formatter_class=argparse.RawTextHelpFormatter)

        self.import_parsers = self.import_parser.add_subparsers(help="Choose which item to import.")

        # ===== Import Car ===== #

        self.import_car_parser = self.import_parsers.add_parser('car')

        # ===== Import Collection ===== #

        self.import_collection_parser = self.import_parsers.add_parser('collection')

        self.import_collection_parser.add_argument('--car',
                                                   metavar="PARENT_CAR_NAME",
                                                   type=str,
                                                   required=True)

        # ===== Import Component ===== #

        self.import_component_parser = self.import_parsers.add_parser('component')

        self.import_component_parser.add_argument('--car',
                                                  metavar="PARENT_CAR_NAME",
                                                  type=str,
                                                  required=True)

        self.import_component_parser.add_argument('--collection',
                                                  metavar="PARENT_COLLECTION_NAME",
                                                  type=str,
                                                  required=True)

        self.add_path_arg()
        self.add_nochild_arg()
        

class ExportSubparser(Subparser):
    def __init__(self, parser_parent):
        self.parser_parent = parser_parent

    def add_path_arg(self):
        for sp_name, sp_obj in list(self.export_parsers.choices.items()):
            sp_obj.add_argument('path',
                                metavar="SAVE_LOCATION",
                                help="System path leading to file that you want to export. "
                                     "Valid formats: [.json, .txt, .csv]",
                                type=str)

    def add_nochild_arg(self):
        for sp_name, sp_obj in list(self.export_parsers.choices.items())[1::]:
            sp_obj.add_argument('--nochildren',
                                help="Import item without child elements.",
                                action='store_true')

    def add_values_arg(self):
        for sp_name, sp_obj in list(self.export_parsers.choices.items()):
            sp_obj.add_argument('--values',
                                help="Select which values to export. All by default.",
                                metavar='VALUES TO EXPORT',
                                dest='values',
                                nargs='*',
                                default=[]
                                )

    def create_subparser(self):
        self.export_parser = self.parser_parent.subparsers.add_parser('export',
                                                                      help="Export item to file.",
                                                                      formatter_class=argparse.RawTextHelpFormatter)

        self.export_parsers = self.export_parser.add_subparsers(help="Choose which item to export.")

        # ===== Export Car ===== #

        self.export_car_parser = self.export_parsers.add_parser('car')

        self.export_car_parser.add_argument('--name',
                                            metavar="CAR_NAME",
                                            type=str,
                                            required=True)

        # ===== Export Collection ===== #

        self.export_collection_parser = self.export_parsers.add_parser('collection')

        self.export_collection_parser.add_argument('--name',
                                                   metavar="COLLECTION_NAME",
                                                   type=str,
                                                   required=True)

        self.export_collection_parser.add_argument('--car',
                                                   metavar="PARENT_CAR_NAME",
                                                   type=str,
                                                   required=True)

        # ===== Export Component ===== #

        self.export_component_parser = self.export_parsers.add_parser('component')

        self.export_component_parser.add_argument('--name',
                                                  metavar="COMPONENT_NAME",
                                                  type=str,
                                                  required=True)

        self.export_component_parser.add_argument('--car',
                                                  metavar="PARENT_CAR_NAME",
                                                  type=str,
                                                  required=True)

        self.export_component_parser.add_argument('--collection',
                                                  metavar="PARENT_COLLECTION_NAME",
                                                  type=str,
                                                  required=True)

        self.add_path_arg()
        self.add_nochild_arg()
        self.add_values_arg()
