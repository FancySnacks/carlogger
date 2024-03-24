"""Depicts a single maintenance, checkup or work done on a specific car component."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from carlogger.items.car_component import CarComponent
from carlogger.items.entry_category import EntryCategory


@dataclass(order=True)
class LogEntry:
    """Depicts a single maintenance, checkup or work done on a specific car component."""

    desc: str
    date: tuple[int, int, int]
    mileage: int
    category: EntryCategory
    tags: list[str]
    component: CarComponent
    _id: str

    @property
    def id(self) -> str:
        return self._id

    def to_json(self) -> dict:
        return self.__dict__()

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        return f"[{self.date}] {self.desc} [Mileage: {self.mileage}] " \
               f"[Type: {self.category}] [{self.tags}] [{self.id}]"

    def __dict__(self) -> dict:
        d = {
            'desc': self.desc,
            'date': self.date,
            'mileage': self.mileage,
            'category': self.category.name,
            'tags': self.tags,
            'component': self.component.name,
            'id': self.id
        }

        return d

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, LogEntry):
            return self.id == other.id
        return NotImplemented
