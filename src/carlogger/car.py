"""Represents a single car containing car info, all the collections, parts and entry logs"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from carlogger.util import format_date_string_to_tuple, create_car_dir_path
from carlogger.car_info import CarInfo
from carlogger.component_collection import ComponentCollection
from carlogger.car_component import CarComponent
from carlogger.log_entry import LogEntry


@dataclass
class Car:
    """Contains car's general manufacturer info, mileage, year of make and it's own entry logs."""
    car_info: CarInfo
    collections: list[ComponentCollection] = field(default_factory=list)
    path: Path = ""

    def __post_init__(self):
        if self.path == "":
            self._create_path()


    def get_all_entry_logs(self) -> list[LogEntry]:
        """Get ALL log entries regarding this car.\n
        NOTE: it's a heavy operation, use it sparingly."""
        entries = [collection.get_all_log_entries(collection.children) for collection in self.collections]
        entries_joined = []
        [entries_joined.extend(entry_list) for entry_list in entries]

        return sorted(entries_joined, key=lambda entry: format_date_string_to_tuple(entry.date))

    def create_collection(self, name: str) -> ComponentCollection:
        """Create new collection, add it to the list and return object reference."""
        new_collection = ComponentCollection(name, path=self.path.joinpath("collections"))
        self.collections.append(new_collection)

        return new_collection

    def get_collection_by_name(self, name: str) -> ComponentCollection | None:
        """Find and return collection by name."""
        for collection in self.collections:
            if collection.name == name:
                return collection

        return None

    def get_component_by_name(self, name: str) -> CarComponent | None:
        """Find and return component by name looping through all collections."""
        for collection in self.collections:
            for child in collection.children:
                if child.name == name:
                    return child

        return None

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        result = ''
        info = vars(self.car_info)
        info.pop('path')

        for key, val in info.items():
            result += f"{key}: {val} \n"

        return result

    def _create_path(self):
        self.path = create_car_dir_path(self.car_info.to_json())
