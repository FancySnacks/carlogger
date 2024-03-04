"""Manage car save directories."""

import os
import shutil

from carlogger.car import Car
from carlogger.filedata_manager import FiledataManager
from carlogger.component_collection import ComponentCollection
from carlogger.car_component import CarComponent
from carlogger.car_info import CarInfo
from carlogger.const import CARS_PATH
from carlogger.util import get_car_dirs


class DirectoryManager:
    def __init__(self, data_manager: FiledataManager):
        self.data_manager = data_manager

    def create_car_directory(self, car: Car):
        path = car.path
        data_path = self.create_car_info_path(car)
        self._create_car_dir(path)
        self.data_manager.save_file(car.car_info, data_path)

    def create_car_info_path(self, car: Car):
        return car.path.joinpath(f"{car.car_info.name}.{self.data_manager.suffix}")

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

    def update_car_directory(self, car: Car):
        self.data_manager.save_file(car.car_info, self.create_car_info_path(car))
        self.update_collections_files(car.collections)

    def update_collections_files(self, comp_collections: list[ComponentCollection]):
        for coll in comp_collections:
            self.data_manager.save_file(coll, coll.get_target_path(self.data_manager.suffix))
            self.update_components_files(coll.children)

    def update_components_files(self, comp_list: list[CarComponent]):
        for comp in comp_list:
            self.data_manager.save_file(comp, comp.get_target_path(self.data_manager.suffix))

    def load_car_dir(self, car_name: str):
        """Load target car inside 'save' folder via name."""
        car_dirs = get_car_dirs()

        if car_name in car_dirs:
            path = CARS_PATH.joinpath(car_name)
            car_info = CarInfo(**self.data_manager.load_file(self._create_car_info_path(path)))

            collections = self.load_car_collections_from_path(path)

            new_car = Car(car_info, collections=collections, path=path)

            return new_car

        raise NotADirectoryError(f"'{car_name}' directory not found in save folder")

    def load_all_car_dir(self) -> list[Car]:
        """Load all saved cars inside 'save' folder and return them as list of objects."""
        cars: list[Car] = []
        car_dirs = get_car_dirs()

        for directory in car_dirs:
            path = CARS_PATH.joinpath(directory)
            car_info = CarInfo(**self.data_manager.load_file(self._create_car_info_path(path)))

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

        for child in collection.children:
            comp_data = self.data_manager.load_file(child['path'])
            c = CarComponent(comp_data['name'], collection.path.joinpath('components'))
            coms.append(c)

        return coms

    def _create_car_info_path(self, dir_path):
        a = dir_path.joinpath(f"{dir_path.name}.{self.data_manager.suffix}")
        return a
