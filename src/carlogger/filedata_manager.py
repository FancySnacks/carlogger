"""Save and load collections, components, logs."""

import json
import os

from abc import ABC, abstractmethod
from typing import Protocol


class JSONSerializableObject(Protocol):
    """Object that implements `to_json` function."""
    def to_json(self) -> dict:
        """Transforms initialized object to JSON-serializable dictionary to be saved into a file."""
        pass

    def get_target_path(self, extension: str) -> str:
        pass


class FiledataManager(ABC):
    """Abstract implementation of class that loads and saves data to files."""

    suffix = ""

    @abstractmethod
    def load_file(self, filepath):
        """Load data from target file."""
        pass

    @abstractmethod
    def save_file(self, obj, filepath=None, *values):
        """Save data as file to target path."""
        pass

    @abstractmethod
    def delete_file(self, obj):
        """Remove file from the system."""
        pass

    @abstractmethod
    def delete_file_raw(self, path: str):
        """Remove file from the system."""
        pass

    @abstractmethod
    def export_selected_values(self, keys_to_export, data_to_save):
        return


class JSONFiledataManager(FiledataManager):
    suffix = "json"

    def load_file(self, filepath) -> dict:
        """Load data from target JSON file."""
        with open(filepath, "r") as file:
            return json.load(file)

    def save_file(self, obj: JSONSerializableObject, filepath=None, *values):
        """Converts object to a dictionary to be saved to target path in a JSON file."""
        data_to_save: dict = obj.to_json()
        if values:
            data_to_save = self.export_selected_values(values, data_to_save)

        if filepath is None:
            filepath = obj.get_target_path(self.suffix)

        with open(filepath, "w+") as file:
            json.dump(data_to_save, file, indent=3)

    def delete_file(self, obj: JSONSerializableObject):
        """Remove target savefile from the system."""
        os.remove(obj.get_target_path(self.suffix))

    def delete_file_raw(self, filepath: str):
        os.remove(filepath)

    def export_selected_values(self, keys_to_export, data_to_save: dict):
        values_to_export = {}
        for key in data_to_save.keys():
            if key in keys_to_export:
                values_to_export[key] = data_to_save[key]
        data_to_save = values_to_export

        return data_to_save


class TxtFiledataManager(FiledataManager):
    suffix = "txt"

    def load_file(self, filepath) -> list[str]:
        """Load data from target txt file."""
        with open(filepath, "r") as file:
            return file.readlines()

    def save_file(self, obj, filepath=None, *values):
        """Save item to target path as a txt file."""
        data_to_save: dict = obj.to_json()

        if values:
            data_to_save = self.export_selected_values(*values, data_to_save)

        if filepath is None:
            filepath = obj.get_target_path(self.suffix)

        with open(filepath, "w+") as file:
            file.write(str(data_to_save))

    def delete_file(self, obj):
        """Remove target savefile from the system."""
        os.remove(obj.get_target_path(self.suffix))

    def delete_file_raw(self, filepath: str):
        os.remove(filepath)

    def export_selected_values(self, keys_to_export, data_to_save: dict):
        values_to_export = {}
        for key in data_to_save.keys():
            if key in keys_to_export:
                values_to_export[key] = data_to_save[key]
        data_to_save = values_to_export

        return data_to_save
