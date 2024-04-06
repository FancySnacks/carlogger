"""Car component collection identifiable by category"""

from __future__ import annotations

import pathlib

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from carlogger.items.car import Car

from dataclasses import dataclass, field

from carlogger.items.car_component import CarComponent
from carlogger.const import ADD_COMPONENT_SUCCESS, ADD_COMPONENT_FAILURE, \
    REMOVE_COMPONENT_SUCCESS, REMOVE_COMPONENT_FAILURE, ADD_COLLECTION_FAILURE, REMOVE_COLLECTION_FAILURE, \
    REMOVE_COLLECTION_SUCCESS
from carlogger.items.log_entry import LogEntry


@dataclass
class ComponentCollection:
    """Contains multiple CarComponent OR ComponentCollection classes identified by a single category,
    example: engine group.\n
    Adding more ComponentCollection classes to 'components' list allows for more specific grouping.\n
    For example user could want to have 'engine' collection and have various parts as part of this collection or,
    he might wish to be more specific and create additional collections like 'ignition', 'exhaust', 'crankshaft'
    which hold actual CarComponent classes.
    """

    name: str
    components: list[CarComponent] = field(default_factory=list)
    collections: list[ComponentCollection] = field(default_factory=list)
    car: Car = None
    parent_collection: ComponentCollection = None
    path: str = ""

    def __post_init__(self):
        self.path = pathlib.Path(self.path)
        self.components = [] if self.components is None else self.components
        self.collections = [] if self.collections is None else self.collections

    @property
    def children(self) -> list:
        return self.collections + self.components

    def get_all_components(self) -> list[CarComponent]:
        """Returns all CarComponent items from all components collections."""
        n = [coll.children for coll in self.collections]
        e = []
        [e.extend(item) for item in n]
        return e + self.components

    def get_all_log_entries(self) -> list[LogEntry]:
        """Returns all log entries from components CarComponent objects from all components collections."""
        components = self.get_all_components()
        entries = [comp.log_entries for comp in components]
        joined_entries = []
        [joined_entries.extend(e) for e in entries]

        return joined_entries

    def create_component(self, name: str) -> CarComponent:
        """Create new car component, add it to the list and return object reference."""
        self._check_for_component_duplicates(name)
        new_component = CarComponent(name, path=self.path.parent.joinpath('components'))
        self.components.append(new_component)

        print(ADD_COMPONENT_SUCCESS.format(name=name))

        return new_component

    def delete_component(self, name: str):
        component_to_remove = self.get_component_by_name(name)

        if component_to_remove:
            self.components.remove(component_to_remove)
            print(REMOVE_COMPONENT_SUCCESS.format(name=name))
        else:
            print(REMOVE_COMPONENT_FAILURE.format(name=name, collection=self.name))

    def delete_collection(self, name: str):
        collection_to_remove = self.get_collection_by_name(name)

        if collection_to_remove:
            self.collections.remove(collection_to_remove)
    def delete_components(self):
        for child in self.components:
            self.delete_component(child.name)
        self.components = []

    def delete_collections(self):
        for child in self.collections:
            self.delete_collection(child.name)
        self.collections = []

    def delete_children(self):
        self.delete_components()
        self.delete_collections()

    def _check_for_nested_collection_duplicates(self, name: str):
        if name in [ch.name for ch in self.components]:
            raise ValueError(ADD_COLLECTION_FAILURE.format(name=name, car=self.car.car_info.name))

    def _check_for_component_duplicates(self, name: str):
        if name in [ch.name for ch in self.components]:
            raise ValueError(ADD_COMPONENT_FAILURE.format(name=name, collection=self.name))

    def get_component_by_name(self, name: str) -> CarComponent:
        """Find and return car component of this collection by name."""
        for comp in self.components:
            if comp.name == name:
                return comp

        raise ValueError(f"ERROR: Component '{name}' was not found in '{self.name}' collection!")

    def get_collection_by_name(self, name: str) -> ComponentCollection:
        """Find and return nested component collection by name."""
        for child in self.collections:
            if child.name == name:
                return child

        raise ValueError(f"ERROR: Component collection '{name}' was not found in '{self.name}' collection!")
    
    def to_json(self) -> dict:
        d = {'name': self.name,
             'parent_collection': self._get_parent_collection_path(self.parent_collection),
             'collections': [self._create_child_collection_reference(child, "json") for child in self.collections],
             'components': [self._create_child_reference(child, "json") for child in self.components]
             }
        return d

    def _get_parent_collection_path(self, parent_collection: ComponentCollection) -> str:
        if parent_collection not in (None, ""):
            return str(self.parent_collection.get_target_path("json"))
        else:
            return ""

    def _create_child_reference(self, obj: CarComponent | ComponentCollection, extension: str) -> dict:
        return {'name': obj.name, 'path': str(obj.get_target_path(extension))}

    def _create_child_collection_reference(self, obj: ComponentCollection, extension: str) -> dict:
        return {'name': obj.name,
                'path': str(obj.get_target_path(extension))}

    def get_target_path(self, extension: str) -> str:
        """Extension without the dot"""
        return self.path.joinpath(f"{self.name.replace(' ', '_')}.{extension}")

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        result = f"{self.name} ({len(self.components)}): \n"

        for element in self.components:
            result += f"{element.name}\n"

        return result

    def __repr__(self) -> str:
        return f"[COLLECTION] {self.name} {len(self.components)} " \
               f"Components | {len(self.collections)} Nested Collections"
