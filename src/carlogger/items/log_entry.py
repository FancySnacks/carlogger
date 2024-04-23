"""Depicts a single maintenance, checkup or work done on a specific car component."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from carlogger.items.car_component import CarComponent
from carlogger.items.entry_category import EntryCategory
from carlogger.const import TODAY
from carlogger.util import date_string_to_date, format_date_struct_to_tuple, format_tuple_to_date_string


@dataclass(order=True)
class LogEntry:
    """Depicts a single maintenance, checkup or work done on a specific car component."""

    desc: str
    date: str
    mileage: int
    category: EntryCategory
    tags: list[str]
    component: CarComponent
    _id: str
    custom_info: dict[str, ...] = field(default_factory=dict)

    @property
    def id(self) -> str:
        return self._id

    def to_json(self) -> dict:
        return self.__dict__()

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        return f"[{self.date}] {self.desc} [Mileage: {self.mileage}] " \
               f"[Type: {self.category}] [{self.id}]\n"

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

        for k, v in self.custom_info.items():
            d[k] = v

        return d

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, LogEntry):
            return self.id == other.id
        return NotImplemented


@dataclass(order=True)
class ScheduledLogEntry(LogEntry):
    """LogEntry but scheduled in time based on date or target mileage and ability to be repeatable."""

    day_frequency: int = 1
    repeating: bool = False

    def __post_init__(self):
        self.repeat()

    def repeat(self):
        self.date = self.get_new_date()

    def get_new_date(self) -> str:
        old_date = date_string_to_date(self.date)
        new_date = old_date + datetime.timedelta(days=self.day_frequency)
        new_date = (new_date.day, new_date.month, new_date.year)
        return format_tuple_to_date_string(new_date)

    def get_days_remaining(self) -> int:
        date = date_string_to_date(self.date)
        days = date - date_string_to_date(TODAY)
        return abs(days.days)

    def get_mileage_remaining(self) -> int:
        return self.mileage - self.component.current_mileage

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        return f"[{self.date}] [in {self.get_days_remaining()} days] {self.desc} [Mileage: {self.mileage}] " \
               f"[Type: {self.category}] [{self.id}]\n"
