"""Entrance point of this project"""

from carlogger.session import AppSession
from carlogger.argparser import ArgParser
from carlogger.directory_manager import DirectoryManager
from carlogger.filedata_manager import JSONFiledataManager
from carlogger.car_info import CarInfo
from carlogger.log_entry import LogEntry
from carlogger.car_component import CarComponent


def main(argv: list[str] = None) -> int:
    parser = ArgParser()
    parser.setup_args()
    parsed_args: dict = parser.parse_args(argv)

    data_manager = JSONFiledataManager()
    directory_manager = DirectoryManager(data_manager)

    if car := parsed_args.get('car'):
        loaded_car = directory_manager.load_car_dir(car)
        print(loaded_car)


    # new_car = CarInfo(manufacturer='Seat',
    #                   model='Leon 1',
    #                   year=2003,
    #                   body='hatchback',
    #                   length=4140,
    #                   mileage=205000,
    #                   weight=1700,
    #                   name='Daily')
    #
    # new_entry = {"desc": "Engine Checkup",
    #              "date": "09-03-1964",
    #              "mileage": 1404,
    #              "category": "check",
    #              "tags": [],
    #              }
    #
    # cars = directory_manager.load_all_car_dir()

    app = AppSession(directory_manager)
    # app.cars = cars

    # print(app.cars)

    #app.remove_car("Daily")

    # create a new app session
    # load saved info: car -> collections -> car parts -> entries
    # create widgets

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
