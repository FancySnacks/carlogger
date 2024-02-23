"""Save and load logs from savefile."""

import json

from abc import ABC, abstractmethod
from typing import Protocol


class JSONSerializableObject(Protocol):
    """Object that implements `to_json` function."""
    def to_json(self) -> dict:
        """Transforms initialized object to JSON-serializable dictionary to be saved into a file."""
        pass

    def get_target_path(self) -> str:
        pass


class FiledataManager(ABC):
    """Abstract implementation of class that loads and saves data to files."""
    @abstractmethod
    def load_file(self, filepath: str):
        """Load data from target file."""
        pass

    @abstractmethod
    def save_file(self, data, filepath: str):
        """Save data as file to target path."""
        pass


class JSONFiledataManager(FiledataManager):
    def load_file(self, filepath: str) -> dict:
        """Load data from target JSON file."""
        with open(filepath, "r") as file:
            return json.load(file)

    def save_file(self, obj: JSONSerializableObject, filepath: str = None):
        """Converts object to a dictionary to be saved to target path in a JSON file."""
        data_to_save: dict = obj.to_json()

        if filepath is None:
            filepath = obj.get_target_path()

        with open(filepath, "w+") as file:
            json.dump(data_to_save, file, indent=3)
