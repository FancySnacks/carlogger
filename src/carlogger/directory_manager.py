"""Manage car save directories."""

import os
import shutil

from carlogger.car import Car
from carlogger.filedata_manager import FiledataManager


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
            os.mkdir(path)
            os.mkdir(path.joinpath("collections"))
            os.mkdir(path.joinpath("components"))
        except FileExistsError:
            return

    def remove_car_directory(self, car: Car):
        path = car.path

        try:
            shutil.rmtree(path)
        except OSError:
            return
