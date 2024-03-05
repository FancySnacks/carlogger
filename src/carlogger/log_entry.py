"""Depicts a single maintenance, checkup or work done on a specific car component."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from carlogger.car_component import CarComponent
from carlogger.entry_category import EntryCategory


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

    def __dict__(self) -> dict:
        d = {
            'desc': self.desc,
            'date': self.date,
            'mileage': self.mileage,
            'category': self.category.name,
            'tags': self.tags,
            'component': self.component.name,
            'id': self._id
        }

        return d

    def __repr__(self):
        return f"[{self.date}] {self.desc} [Mileage: {self.mileage}] [Type: {self.category}] [{self.tags}] [{self.id}]"
