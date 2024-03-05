"""Car component collection identifiable by category"""

from __future__ import annotations

import pathlib

from dataclasses import dataclass, field

from carlogger.car_component import CarComponent
from carlogger.log_entry import LogEntry


@dataclass
class ComponentCollection:
    """Contains multiple CarComponent OR ComponentCollection classes identified by a single category,
    example: engine group.\n
    Adding more ComponentCollection classes to 'children' list allows for more specific grouping.\n
    For example user could want to have 'engine' collection and have various parts as part of this collection or,
    he might wish to be more specific and create additional collections like 'ignition', 'exhaust', 'crankshaft'
    which hold actual CarComponent classes.
    """

    name: str
    children: list[ComponentCollection | CarComponent] = field(default_factory=list)
    path: str = ""

    def __post_init__(self):
        self.path = pathlib.Path(self.path)

    def get_all_components(self,  list_to_search: list, buffer_list: list = None) -> list[CarComponent]:
        """Returns all CarComponent items from all children collections."""
        if buffer_list is None:
            buffer_list = []

        for c in list_to_search:
            if type(c) == CarComponent:
                buffer_list.append(c)
            elif type(c) == ComponentCollection:
                self.get_all_components(c.children, buffer_list)
            else:
                continue

        return buffer_list

    def get_all_log_entries(self,  list_to_search: list, buffer_list: list = None) -> list[LogEntry]:
        """Returns all log entries from children CarComponent objects from all children collections."""
        if buffer_list is None:
            buffer_list = []

        for c in list_to_search:
            if type(c) == CarComponent:
                if len(c.log_entries) > 0:
                    buffer_list.extend(c.log_entries)
            elif type(c) == ComponentCollection:
                self.get_all_log_entries(c.children, buffer_list)
            else:
                continue

        return buffer_list

    def create_component(self, name: str) -> CarComponent:
        """Create new car component, add it to the list and return object reference."""
        new_component = CarComponent(name, path=self.path.parent.joinpath('components'))
        self.children.append(new_component)

        return new_component

    def get_component_by_name(self, name: str) -> CarComponent:
        """Find and return car component of this collection by name."""
        for child in self.children:
            if child.name == name and type(child) == CarComponent:
                return child
    
    def to_json(self) -> dict:
        d = {'name': self.name,
             'children': [self._create_child_reference(child, "json") for child in self.children]
             }

        return d

    def _create_child_reference(self, obj: CarComponent | ComponentCollection, extension: str) -> dict:
        return {'name': obj.name, 'path': str(obj.get_target_path(extension))}

    def get_target_path(self, extension: str) -> str:
        """Extension without the dot"""
        return self.path.joinpath(f"{self.name.replace(' ', '_')}.{extension}")

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        result = f"{self.name} ({len(self.children)}): \n"

        for element in self.children:
            result += f"{element.name}\n"

        return result
