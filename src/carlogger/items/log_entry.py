"""Depicts a single maintenance, checkup or work done on a specific car component."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from carlogger.const import TODAY

if TYPE_CHECKING:
    from carlogger.items.car_component import CarComponent
from carlogger.items.entry_category import EntryCategory
from carlogger.util import date_string_to_date, days_between_date_strings, \
    format_tuple_to_date_string, date_n_days_from_now


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
    """LogEntry but scheduled in time based on date or target mileage and ability to be repeatable.
    When creating a 'late' entry (in a past manner) the 'day_frequency' value should be 0."""

    day_frequency: int = 1
    repeating: bool = False

    def __post_init__(self):
        print(f"1 {self.date}")
        self.repeat()
        print(f"2 {self.date}")

    def repeat(self):
        self.date = self.get_new_date()

    def get_new_date(self) -> str:
        old_date = date_string_to_date(self.date)
        new_date = old_date + datetime.timedelta(days=self.day_frequency)
        new_date = (new_date.day, new_date.month, new_date.year)
        return format_tuple_to_date_string(new_date)

    def get_days_remaining(self) -> int:
        return days_between_date_strings(self.date, TODAY)

    def get_mileage_remaining(self) -> int:
        return self.mileage - self.component.current_mileage

    def days_remaining_to_str(self) -> str:
        """Get remaining days until scheduled entry and return a formatted informative string"""
        days = self.get_days_remaining()

        if self.get_days_remaining() > 0:
            return f"in {days} days"
        elif self.get_days_remaining() < 0:
            return f"{abs(days)} days ago"
        else:
            return ""

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        return f"[{self.date}] [{self.days_remaining_to_str()}] {self.desc} [Mileage: {self.mileage}] " \
               f"[Type: {self.category}] [{self.id}]\n"
