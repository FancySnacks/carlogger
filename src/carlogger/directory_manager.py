"""Manage car save directories."""

import os
import pathlib
import shutil

from carlogger.items.car import Car
from carlogger.filedata_manager import FiledataManager
from carlogger.items.component_collection import ComponentCollection
from carlogger.items.car_component import CarComponent
from carlogger.items.car_info import CarInfo
from carlogger.const import CARS_PATH, ADD_CAR_SUCCESS, ADD_CAR_FAILURE, REMOVE_CAR_SUCCESS, REMOVE_CAR_FAILURE
from carlogger.util import get_car_dirs


class DirectoryManager:
    def __init__(self, data_manager: FiledataManager, car_save_dir=CARS_PATH):
        self.data_manager = data_manager
        self.car_save_dir = car_save_dir

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
            print(ADD_CAR_FAILURE.format(name=path.name, path=path))
            return
        else:
            print(ADD_CAR_SUCCESS.format(name=path.name, path=path))

    def remove_car_directory(self, car: Car):
        """Delete a car directory along with all its data files from 'save' directory if it exists."""
        path = car.path
        try:
            shutil.rmtree(path)
            print(REMOVE_CAR_SUCCESS.format(name=car.car_info.name))
        except OSError:
            print(REMOVE_CAR_FAILURE.format(name=car.car_info.name))
            return

    def remove_item(self, item):
        self.data_manager.delete_file(item)

    def update_car_directory(self, car: Car):
        self.data_manager.save_file(car.car_info, self.create_car_info_path(car))
        self.update_collections_files(car.collections)

    def rename_car_dir(self, car: Car, legacy_car_info_path: str):
        os.remove(legacy_car_info_path)
        self.update_car_directory(car)
        os.rename(car.path, car.path.parent.joinpath(car.car_info.name))

    def update_collections_files(self, comp_collections: list[ComponentCollection]):
        for coll in comp_collections:
            self.data_manager.save_file(coll, coll.get_target_path(self.data_manager.suffix))
            self.update_components_files(coll.components)

    def update_components_files(self, comp_list: list[CarComponent]):
        for comp in comp_list:
            self.data_manager.save_file(comp, comp.get_target_path(self.data_manager.suffix))

    def load_car_dir(self, car_name: str):
        """Load target car inside 'save' folder via name."""
        car_dirs = get_car_dirs(self.car_save_dir)

        if car_name in car_dirs:
            path = self.car_save_dir.joinpath(car_name)
            car_info = CarInfo(**self.data_manager.load_file(self._create_car_info_path(path)))

            new_car = Car(car_info, path=path)
            collections = self.load_car_collections_from_path(path, new_car)
            new_car.collections = collections

            for coll in new_car.collections:
                if coll.parent_collection != "":
                    coll.parent_collection = new_car.get_collection_by_name(pathlib.Path(coll.parent_collection).stem)

            return new_car

        raise NotADirectoryError(f"'{car_name}' directory not found in save folder")

    def load_all_car_dir(self) -> list[Car]:
        """Load all saved cars inside 'save' folder and return them as list of objects."""
        cars: list[Car] = []
        car_dirs = get_car_dirs()

        for directory in car_dirs:
            path = self.car_save_dir.joinpath(directory)
            car_info = CarInfo(**self.data_manager.load_file(self._create_car_info_path(path)))

            new_car = Car(car_info, path=path)
            collections = self.load_car_collections_from_path(path, new_car)
            new_car.collections = collections
            cars.append(new_car)

            for car in cars:
                for coll in car.collections:
                    if coll.parent_collection != "":
                        coll.parent_collection = new_car.get_collection_by_name(coll.parent_collection.split()[-2])

        return cars

    def load_car_collections_from_path(self, path, parent_car: Car = None) -> list[ComponentCollection]:
        """Load collections from target car directory and return them as list."""
        collections = []
        collections_path = path.joinpath("collections")

        try:
            for coll in os.listdir(collections_path):
                collection_data = self.data_manager.load_file(collections_path.joinpath(coll))
                new_collection = ComponentCollection(**collection_data, path=collections_path, car=parent_car)
                components = self.load_car_components_from_path(new_collection)
                new_collection.collections = \
                    [ComponentCollection(name=data.get('name'),
                                         collections=data.get('collections'),
                                         components=data.get('components'),
                                         parent_collection=data.get('parent_collection'),
                                         car=parent_car)
                     for data in new_collection.collections]
                new_collection.components.clear()

                for c in new_collection.collections:
                    c.path = collections_path

                for comp in components:
                    new_collection.components.append(comp)

                collections.append(new_collection)

            return collections

        except FileNotFoundError:
            return []

    def load_car_components_from_path(self, collection: ComponentCollection) -> list[CarComponent]:
        coms = []

        for child in collection.children:
            try:
                if "collections" not in child['path']:
                    item_data: dict = self.data_manager.load_file(child['path'])
                    c = CarComponent(item_data['name'], collection.path.parent.joinpath('components'))
                    self._add_entries_to_component(item_data, c)
                    coms.append(c)

            except FileNotFoundError:
                continue
        return coms

    def _add_entries_to_component(self, comp_data: dict, component_ref: CarComponent):
        for entry in comp_data.get('log_entries'):
            component_ref.create_entry_from_file(entry)


    def _create_car_info_path(self, dir_path):
        a = dir_path.joinpath(f"{dir_path.name}.{self.data_manager.suffix}")
        return a
