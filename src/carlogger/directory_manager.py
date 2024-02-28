"""Manage car save directories."""

import os
import shutil

from carlogger.car import Car
from carlogger.filedata_manager import FiledataManager
from carlogger.const import CARS_PATH


class DirectoryManager:
    def __init__(self, data_manager: FiledataManager):
        self.data_manager = data_manager

    def create_car_directory(self, car: Car):
        path = car.path
        data_path = car.path.joinpath(f"{car.car_info.name}.{self.data_manager.suffix}")
        self._create_car_dir(path)
        self.data_manager.save_file(car.car_info, data_path)

    def _create_car_dir(self, path):
        """Create a new car save directory if it doesn't exist."""
        try:
            print(path)
            os.mkdir(path)
            os.mkdir(path.joinpath("collections"))
            os.mkdir(path.joinpath("components"))
        except FileExistsError:
            return

    def remove_car_directory(self, car: Car):
        """Delete a car directory along with all its data files from 'save' directory if it exists."""
        path = car.path

        try:
            shutil.rmtree(path)
        except OSError:
            return

    def load_all_car_dir(self) -> list[Car]:
        """Load all saved cars inside 'save' folder and return them as list of objects."""
        cars: list[Car] = []
        car_dirs = list(filter(lambda x: os.path.isdir(CARS_PATH.joinpath(x)), os.listdir(CARS_PATH)))

        for directory in car_dirs:
            path = CARS_PATH.joinpath(directory)
            car_info = self.data_manager.load_file(self._create_car_info_path(path))
            cars.append(Car(car_info,
                            path=path))

        return cars

    def _create_car_info_path(self, dir_path):
        a = dir_path.joinpath(f"{dir_path.name}.{self.data_manager.suffix}")
        return a
