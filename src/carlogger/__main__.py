"""Entrance point of this project"""

import sys

from carlogger.gui.root_window import RootWindow
from carlogger.session import AppSession
from carlogger.cli.arg_parser import ArgParser
from carlogger.directory_manager import DirectoryManager
from carlogger.filedata_manager import JSONFiledataManager


def main(argv: list[str] = None) -> int:
    raw_args = sys.argv

    parser = ArgParser()
    parser.setup_args()

    parsed_args: dict = parser.parse_args(argv)

    data_manager = JSONFiledataManager()
    directory_manager = DirectoryManager(data_manager)
    app = AppSession(directory_manager)

    app.execute_console_args(parser.get_subparser_type(raw_args), parsed_args, raw_args)

    if parsed_args.get('gui'):
        app.create_gui(RootWindow())

    if parsed_args.get('printargs'):
        print(parsed_args)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
