"""Save and load logs from savefile."""

import os
import json

from abc import ABC, abstractmethod
from typing import Protocol

from carlogger.car import Car


class JSONSerializableObject(Protocol):
    """Object that implements `to_json` function."""
    def to_json(self) -> dict:
        """Transforms initialized object to JSON-serializable dictionary to be saved into a file."""
        pass

    def get_target_path(self, extension: str) -> str:
        pass


class FiledataManager(ABC):
    """Abstract implementation of class that loads and saves data to files."""
    @abstractmethod
    def load_file(self, filepath):
        """Load data from target file."""
        pass

    @abstractmethod
    def save_file(self, data, filepath):
        """Save data as file to target path."""
        pass


class DataManager(FiledataManager):
    suffix = ""

    @abstractmethod
    def load_file(self, filepath):
        """Load data from target file."""
        pass

    @abstractmethod
    def save_file(self, data, filepath):
        """Save data as file to target path."""
        pass


class JSONFiledataManager(DataManager):
    suffix = "json"

    def load_file(self, filepath) -> dict:
        """Load data from target JSON file."""
        with open(filepath, "r") as file:
            return json.load(file)

    def save_file(self, obj: JSONSerializableObject, filepath=None):
        """Converts object to a dictionary to be saved to target path in a JSON file."""
        data_to_save: dict = obj.to_json()

        if filepath is None:
            filepath = obj.get_target_path(self.suffix)

        with open(filepath, "w+") as file:
            json.dump(data_to_save, file, indent=3)


class CarDirectoryManager(FiledataManager):
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def load_file(self, filepath: str):
        pass

    def save_file(self, data, filepath: str):
        pass

    def create_car_directory(self, car: Car):
        path = car.path
        data_path = car.path.joinpath(f"{car.car_info.name}.{self.data_manager.suffix}")
        self._create_car_dir(path)
        self.data_manager.save_file(car.car_info, data_path)

    def _create_car_dir(self, path):
        try:
            os.mkdir(path)
            os.mkdir(path.joinpath("collections"))
            os.mkdir(path.joinpath("components"))
        except FileExistsError:
            return
