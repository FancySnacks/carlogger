"""Save and load collections, components, logs."""

import json
import os
import shutil

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
    def save_file(self, data, filepath):
        """Save data as file to target path."""
        pass

    @abstractmethod
    def delete_file(self, obj):
        """Remove file from the system."""
        pass


class JSONFiledataManager(FiledataManager):
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

    def delete_file(self, obj: JSONSerializableObject):
        """Remove target savefile from the system."""
        os.remove(obj.get_target_path(self.suffix))
