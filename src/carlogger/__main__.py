"""Entrance point of this project"""

from carlogger.session import AppSession
from carlogger.argparser import ArgParser
from carlogger.filedata_manager import CarDirectoryManager, JSONFiledataManager
from carlogger.car_info import CarInfo


def main(argv: list[str] = None) -> int:
    parser = ArgParser()
    parsed_args: dict = parser.parse_args(argv)

    new_car = CarInfo(name='Daily',
                      manufacturer='Seat',
                      model='Leon 1',
                      year=2003,
                      body='hatchback',
                      length=4140,
                      mileage=205000,
                      weight=1700)

    data_manager = JSONFiledataManager()
    filedata_manager = CarDirectoryManager(data_manager)

    app = AppSession(filedata_manager)
    app.add_new_car(new_car.to_json())

    # create a new app session
    # load saved info: car -> collections -> car parts -> entries
    # create widgets

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
