"""Argument parser for CLI input"""

import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="Car Logger",
                                              usage="carlogger [-args]",
                                              description="description",
                                              epilog="epilog")

    def setup_args(self):
        self.parser.add_argument()
        # --gui argument
        # argument for creating collections
        # argument for creating components
        # argument for creating entries

    def parse_args(self, args: list[str]) -> dict:
        return self.parser.parse_args(args).__dict__
