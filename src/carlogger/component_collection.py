"""Car component collection identifiable by category"""

from __future__ import annotations

from dataclasses import dataclass, field

from carlogger.car_component import CarComponent
from carlogger.log_entry import LogEntry


@dataclass
class ComponentCollection:
    """Contains multiple CarComponent OR ComponentCollection classes identified by a single category,
    example: engine group.\n
    Adding more ComponentCollection classes to 'car_components' list allows for more specific grouping.\n
    For example user could want to have 'engine' collection and have various parts as part of this collection or,
    he might wish to be more specific and create additional collections like 'ignition', 'exhaust', 'crankshaft'
    which hold actual CarComponent classes.
    """

    name: str
    car_components: list[ComponentCollection | CarComponent] = field(default_factory=list)

    def get_all_components(self,  list_to_search: list, buffer_list: list = None) -> list[CarComponent]:
        """Returns all CarComponent items from all children collections."""
        if buffer_list is None:
            buffer_list = []

        for c in list_to_search:
            if type(c) == CarComponent:
                buffer_list.append(c)
            elif type(c) == ComponentCollection:
                self.get_all_components(c.car_components, buffer_list)
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
                self.get_all_log_entries(c.car_components, buffer_list)
            else:
                continue

        return buffer_list
