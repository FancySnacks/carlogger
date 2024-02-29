"""Manage car save directories."""

import os
import shutil

from carlogger.car import Car
from carlogger.filedata_manager import FiledataManager
from carlogger.component_collection import ComponentCollection
from carlogger.car_component import CarComponent
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

            collections = self.load_car_collections_from_path(path)

            cars.append(Car(car_info,
                            collections=collections,
                            path=path))

        return cars

    def load_car_collections_from_path(self, path) -> list[ComponentCollection]:
        """Load collections from target car directory and return them as list."""
        collections = []
        collections_path = path.joinpath("collections")

        for coll in os.listdir(collections_path):
            collection_data = self.data_manager.load_file(collections_path.joinpath(coll))
            new_collection = ComponentCollection(**collection_data, path=collections_path)
            components = self.load_car_components_from_path(new_collection, path)
            new_collection.children.clear()
            
            for comp in components:
                new_collection.children.append(comp)
            
            collections.append(new_collection)

        return collections

    def load_car_components_from_path(self, collection: ComponentCollection, path) -> list[CarComponent]:
        coms = []
        com_path = path.joinpath("components")

        for child in collection.children:
            comp_data = self.data_manager.load_file(child['path'])
            coms.append(CarComponent(**comp_data))

        return coms

    def _create_car_info_path(self, dir_path):
        a = dir_path.joinpath(f"{dir_path.name}.{self.data_manager.suffix}")
        return a
