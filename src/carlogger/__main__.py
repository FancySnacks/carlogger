"""Entrance point of this project"""

from carlogger.session import AppSession
from carlogger.argparser import ArgParser
from carlogger.filedata_manager import JSONFiledataManager


def main(argv: list[str] = None) -> int:
    parser = ArgParser()
    parsed_args: dict = parser.parse_args(argv)

    file_manager = JSONFiledataManager()
    # load cars
    cars = file_manager.load_file()

    app = AppSession(cars)

    # create a new app session
    # load saved info: car -> collections -> car parts -> entries
    # create widgets

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
