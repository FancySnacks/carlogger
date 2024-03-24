"""Represents a single car containing car info, all the collections, parts and entry logs"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from carlogger.const import ADD_COLLECTION_SUCCESS, ADD_COLLECTION_FAILURE, \
    REMOVE_COLLECTION_SUCCESS, REMOVE_COLLECTION_FAILURE
from carlogger.util import format_date_string_to_tuple, create_car_dir_path
from carlogger.items.car_info import CarInfo
from carlogger.items.component_collection import ComponentCollection
from carlogger.items.car_component import CarComponent
from carlogger.items.log_entry import LogEntry


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
        self._check_for_collection_duplicates(name=name)

        new_collection = ComponentCollection(name, car=self, path=self.path.joinpath("collections"))
        self.collections.append(new_collection)
        print(ADD_COLLECTION_SUCCESS.format(name=name))

        return new_collection

    def delete_collection(self, name: str):
        collection_to_remove = self.get_collection_by_name(name)

        if collection_to_remove:
            collection_to_remove.delete_children()
            self.collections.remove(collection_to_remove)

            print(REMOVE_COLLECTION_SUCCESS.format(name=name))
        else:
            print(REMOVE_COLLECTION_FAILURE.format(name=name, car=self.car_info.name))

    def _check_for_collection_duplicates(self, name):
        if name in [coll.name for coll in self.collections]:
            raise ValueError(ADD_COLLECTION_FAILURE.format(name=name, car=self.car_info.name))

    def get_collection_by_name(self, name: str) -> ComponentCollection | None:
        """Find and return collection by name."""
        for collection in self.collections:
            if collection.name == name:
                return collection

        raise ValueError(f"ERROR: Collection '{name}' was not found in '{self.car_info.name}' car!")

    def get_component_by_name(self, name: str) -> CarComponent | None:
        """Find and return component by name looping through all collections."""
        for collection in self.collections:
            for child in collection.children:
                if child.name == name:
                    return child

        return None

    def get_component_of_entry_by_entry_id(self, entry_id: str) -> CarComponent:
        """Find and return LogEntry by unique id looping through all items."""
        entries = self.get_all_entry_logs()

        for entry in entries:
            if entry.id == entry_id:
                return entry.component

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
