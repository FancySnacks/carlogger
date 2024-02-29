"""Represents a single car containing car info, all the collections, parts and entry logs"""

from __future__ import annotations

from functools import lru_cache
from dataclasses import dataclass, field

from carlogger.util import format_date_string_to_tuple, create_car_dir_path

from pathlib import Path
from carlogger.car_info import CarInfo
from carlogger.component_collection import ComponentCollection
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

    @lru_cache(maxsize=10)
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

    def _create_path(self):
        self.path = create_car_dir_path(self.car_info.to_json())
