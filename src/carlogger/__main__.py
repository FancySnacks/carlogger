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
    parsed_args: dict = parser.parse_args(argv)

    new_car = CarInfo(manufacturer='Seat',
                      model='Leon 1',
                      year=2003,
                      body='hatchback',
                      length=4140,
                      mileage=205000,
                      weight=1700,
                      name='Daily')

    data_manager = JSONFiledataManager()
    directory_manager = DirectoryManager(data_manager)
    cars = directory_manager.load_all_car_dir()

    app = AppSession(directory_manager)
    app.cars = cars
    print(app.cars)

    app.add_new_car(new_car.to_json())
    #app.remove_car("Daily")

    # create a new app session
    # load saved info: car -> collections -> car parts -> entries
    # create widgets

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
