"""Represents a single car containing car info, all the collections, parts and entry logs"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from carlogger.printer import Printer
from carlogger.util import format_date_string_to_tuple, create_car_dir_path
from carlogger.items.car_info import CarInfo
from carlogger.items.component_collection import ComponentCollection
from carlogger.items.car_component import CarComponent
from carlogger.items.log_entry import LogEntry, ScheduledLogEntry


@dataclass
class Car:
    """Contains car's general manufacturer info, mileage, year of make and it's own entry logs."""
    car_info: CarInfo
    collections: list[ComponentCollection] = field(default_factory=list)
    path: Path = ""

    def __post_init__(self):
        if self.path == "":
            self._create_path()

    def __getattr__(self, item):
        if item in self.car_info.to_json().keys():
            return self.car_info.to_json()[item]
        else:
            getattr(self, item)

    def get_non_nested_collections(self) -> list[ComponentCollection]:
        """Get only collections belonging to this car that aren't children of other collections."""
        non_nested = filter(lambda coll: coll.parent_collection in (None, ""), self.collections)
        return list(non_nested)

    def get_all_entry_logs(self, include_scheduled=False) -> list[LogEntry]:
        """Get ALL log entries regarding this car.\n
        NOTE: it's a heavy operation, use it sparingly."""
        entries = [collection.get_all_entry_logs(include_scheduled) for collection in self.collections]
        entries_joined = []
        [entries_joined.extend(entry_list) for entry_list in entries]

        return sorted(entries_joined, key=lambda entry: format_date_string_to_tuple(entry.date))

    def get_all_scheduled_entry_logs(self) -> list[ScheduledLogEntry]:
        """Get ALL scheduled log entries regarding this car.\n
        NOTE: it's a heavy operation, use it sparingly."""
        entries = [collection.get_all_scheduled_entry_logs() for collection in self.collections]
        entries_joined = []
        [entries_joined.extend(entry_list) for entry_list in entries]

        return sorted(entries_joined, key=lambda entry: format_date_string_to_tuple(entry.date))

    def get_all_components(self) -> list[CarComponent]:
        comps = [coll.components for coll in self.collections]
        comps_joined = []
        [comps_joined.extend(complist) for complist in comps]
        return comps_joined

    def create_collection(self, name: str) -> ComponentCollection:
        """Create new collection, add it to the list and return object reference."""
        try:
            self._check_for_collection_duplicates(name=name)

            new_collection = ComponentCollection(name, car=self, path=self.path.joinpath("collections"))
            self.collections.append(new_collection)
            Printer.print_msg(new_collection, 'ADD_SUCCESS', name=new_collection.name, relation=self.car_info.name)

            return new_collection
        except Exception:
            Printer.print_msg(ComponentCollection, 'ADD_FAIL', name=name, relation=self.car_info.name)

    def create_nested_collection(self, name: str, parent_collection_name: str) -> ComponentCollection:
        """Create new collection, add it to the list and return object reference."""
        self._check_for_collection_duplicates(name=name)

        parent_collection = self.get_collection_by_name(parent_collection_name)
        new_collection = ComponentCollection(name, car=self, parent_collection=parent_collection,
                                             path=self.path.joinpath("collections"))
        parent_collection.collections.append(new_collection)

        self.collections.append(new_collection)

        Printer.print_msg(new_collection, 'ADD_SUCCESS', name=new_collection.name,
                          relation=f"{self.car_info.name}->{parent_collection.name}")

        return new_collection

    def delete_collection(self, name: str):
        collection_to_remove = self.get_collection_by_name(name)

        if collection_to_remove:

            if parent := collection_to_remove.parent_collection:
                parent.delete_collection(name)

            self.collections.remove(collection_to_remove)

            if parent:
                Printer.print_msg(collection_to_remove,
                                  'DEL_SUCCESS', name=name, relation=f"{self.car_info.name}->{parent.name}")
                return

            Printer.print_msg(collection_to_remove, 'DEL_SUCCESS', name=name, relation=self.car_info.name)
        else:
            Printer.print_msg(ComponentCollection, 'DEL_FAIL', name=name, relation=self.car_info.name)

    def delete_children(self):
        """Clear all collections, components and entry logs."""


    def _check_for_collection_duplicates(self, name):
        if name in [coll.name for coll in self.collections]:
            Printer.print_msg(ComponentCollection, 'ADD_FAIL', name=name,
                              relation=self.car_info.name, reason=" because collection of exact name already exists")

    def get_collection_by_name(self, name: str) -> ComponentCollection | None:
        """Find and return collection by name."""
        for collection in self.collections:
            if collection.name == name:
                return collection

        Printer.print_msg(ComponentCollection, 'READ_FAIL', name=name, relation=self.car_info.name)

    def get_component_by_name(self, name: str) -> CarComponent | None:
        """Find and return component by name looping through all collections."""
        for collection in self.collections:
            for child in collection.children:
                if child.name == name:
                    return child

        Printer.print_msg(CarComponent, 'READ_FAIL', name=name, relation=self.car_info.name)

    def get_entry_by_id(self, entry_id: str) -> LogEntry | ScheduledLogEntry | None:
        entries = self.get_all_entry_logs(include_scheduled=True)
        for entry in entries:
            if entry.id == entry_id:
                return entry

        Printer.print_msg(LogEntry, 'READ_FAIL', name=entry_id, relation=self.car_info.name)

    def get_component_of_entry_by_entry_id(self, entry_id: str) -> CarComponent:
        """Find and return LogEntry by unique id looping through all items."""
        entries = self.get_all_entry_logs(include_scheduled=True)

        for entry in entries:
            if entry.id == entry_id:
                return entry.component

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        result = f'\n=== {self.car_info.name} ===\n'
        info = vars(self.car_info)
        info.pop('path')

        for key, val in info.items():
            result += f"{key}: {val} \n"

        return result

    def _create_path(self):
        self.path = create_car_dir_path(self.car_info.to_json())
