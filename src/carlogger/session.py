"""Class that combines everything together, the heart of the program"""

import os

from carlogger.filedata_manager import CarDirectoryManager
from carlogger.car import Car
from carlogger.car_info import CarInfo
from carlogger.util import create_car_dir_path


class AppSession:
    """Setup current app session, load saved info: load collections, components and log entries."""
    def __init__(self, directory_manager: CarDirectoryManager):
        self.directory_manager = directory_manager

        self.cars: list[Car] = []
        self.selected_car: Car = ...

    def add_new_car(self, car_info: dict):
        car_info = CarInfo(**car_info)
        path = create_car_dir_path(car_info.to_json())

        new_car = Car(car_info=car_info,
                      path=path)

        self.directory_manager.create_car_directory(new_car)

