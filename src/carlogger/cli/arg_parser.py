"""Argument parser for CLI input"""

import argparse

from carlogger.cli.subparser import Subparser, AddSubparser, ReadSubparser, DeleteSubparser, UpdateSubparser, \
    ImportSubparser, ExportSubparser


class ArgParser:
    """Handles console arguments and executes related functions."""
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="Car Logger",
                                              usage="carlogger [-args]",
                                              description="Choose 'carlogger --gui' for visual interface.",
                                              epilog="Made by FancySnacks | 2024 | MIT License",
                                              formatter_class=argparse.RawDescriptionHelpFormatter)
        self.subparsers = self.parser.add_subparsers(help="Subcommands")

        self.subparser_obj: list[Subparser] = []

        self.parsed_args: dict = {}

    def setup_args(self):
        self.parser.add_argument('--gui',
                                 action='store_true',
                                 help="Open graphical user interface for this app.")

        self.parser.add_argument('--printargs',
                                 action='store_true',
                                 help="Print parsed arguments to the console.")

        self.setup_subparsers()

    def setup_subparsers(self):
        self.add_subparser(AddSubparser(self))
        self.add_subparser(ReadSubparser(self))
        self.add_subparser(DeleteSubparser(self))
        self.add_subparser(UpdateSubparser(self))
        self.add_subparser(ImportSubparser(self))
        self.add_subparser(ExportSubparser(self))

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

        if 'update' in argv:
            return 'update'

        if 'import' in argv:
            return 'import'

        if 'export' in argv:
            return 'export'
