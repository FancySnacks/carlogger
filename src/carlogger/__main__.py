"""Entrance point of this project"""

import sys

from carlogger.session import AppSession
from carlogger.cli.arg_parser import ArgParser, Subparser, AddSubparser, ReadSubparser, DeleteSubparser
from carlogger.directory_manager import DirectoryManager
from carlogger.filedata_manager import JSONFiledataManager


def create_subparser(parser_parent: ArgParser, argv: list[str]) -> Subparser | None:
    if 'add' in argv:
        return AddSubparser(parser_parent)

    if 'read' in argv:
        return ReadSubparser(parser_parent)

    if 'delete' in argv:
        return DeleteSubparser(parser_parent)

    return None


def main(argv: list[str] = None) -> int:
    raw_args = sys.argv

    parser = ArgParser()
    parser.setup_args()

    parsed_args: dict = parser.parse_args(argv)

    data_manager = JSONFiledataManager()
    directory_manager = DirectoryManager(data_manager)
    app = AppSession(directory_manager)

    app.execute_console_args(parser.get_subparser_type(raw_args), parsed_args, raw_args)

    print(parsed_args)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
