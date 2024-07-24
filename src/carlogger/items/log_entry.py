"""Depicts a single maintenance, checkup or work done on a specific car component."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from carlogger.const import TODAY

if TYPE_CHECKING:
    from carlogger.items.car_component import CarComponent
from carlogger.items.entry_category import EntryCategory
from carlogger.util import date_string_to_date, days_between_date_strings, format_tuple_to_date_string


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

    def filter_options(self) -> list[str]:
        return ['id', 'desc', 'date', 'component', 'category', 'mileage'] + list(self.custom_info.keys())

    def get_shortened_id(self) -> str:
        div_index = self.id.find('-')
        return self.id[:div_index:]

    def to_json(self) -> dict:
        return self.__dict__()

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        desc = self.desc.replace('\n', ' ')
        return f"[{self.date}] [{self.get_shortened_id()}] {desc} [Mileage: {self.mileage}] [Type: {self.category}]"

    def __dict__(self) -> dict:
        d = {
            'desc': self.desc,
            'date': self.date,
            'mileage': self.mileage,
            'category': self.category.name,
            'tags': self.tags,
            'component': self.component.name,
            'id': self.id,
            'custom_info': self.custom_info
        }

        return d

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, LogEntry):
            return self.id == other.id
        return NotImplemented


@dataclass
class LogEntryScheduleRule(ABC):
    """Abstract class for defining scheduling rule for ScheduledLogEntry class."""
    frequency: int
    parent_log_entry: LogEntry

    @abstractmethod
    def set_new_time(self):
        pass

    @abstractmethod
    def get_time_remaining(self):
        pass

    @abstractmethod
    def get_new_time(self):
        pass

    @abstractmethod
    def time_remaining_to_str(self):
        pass

    @abstractmethod
    def get_formatted_info(self) -> str:
        pass

    @abstractmethod
    def get_schedule_rule(self) -> str:
        return self.__name__


@dataclass
class DateScheduleRule(LogEntryScheduleRule):
    def set_new_time(self):
        self.parent_log_entry.date = self.get_new_time()
        self.parent_log_entry.mileage = self.parent_log_entry.component.current_mileage

    def get_new_time(self) -> str:
        """Get new target mileage for scheduled entry"""
        old_date = date_string_to_date(self.parent_log_entry.date)
        new_date = old_date + datetime.timedelta(days=self.frequency)
        new_date = (new_date.day, new_date.month, new_date.year)
        return format_tuple_to_date_string(new_date)

    def get_time_remaining(self) -> int:
        """Get remaining days until scheduled entry as int"""
        return days_between_date_strings(self.parent_log_entry.date, TODAY)

    def time_remaining_to_str(self) -> str:
        """Get remaining days until scheduled entry and return a formatted informative string"""
        days = self.get_time_remaining()

        if self.get_time_remaining() > 0:
            return f"in {days} days"
        elif self.get_time_remaining() == 0:
            return f"Today"
        elif self.get_time_remaining() < 0:
            return f"{abs(days)} days ago"
        else:
            return ""

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class"""
        return f"[{self.parent_log_entry.date}] [{self.time_remaining_to_str()}] " \
               f"{self.parent_log_entry.desc} [Type: {self.parent_log_entry.category}] [{self.parent_log_entry.id}]"

    def get_schedule_rule(self) -> str:
        return 'date'


@dataclass
class MileageScheduleRule(LogEntryScheduleRule):
    def set_new_time(self):
        self.parent_log_entry.mileage = self.get_new_time()

    def get_new_time(self) -> int:
        """Get new target mileage for scheduled entry"""
        return self.parent_log_entry.component.current_mileage + self.frequency

    def get_time_remaining(self) -> int:
        """Get remaining mileage until scheduled entry as int"""
        return self.parent_log_entry.mileage - self.parent_log_entry.component.current_mileage

    def time_remaining_to_str(self) -> str:
        """Get remaining mileage until scheduled entry and return a formatted informative string"""
        mileage_remaining = self.get_time_remaining()

        if self.get_time_remaining() > 0:
            return f"-{mileage_remaining}"
        elif self.get_time_remaining() < 0:
            return f"+{abs(mileage_remaining)}"
        else:
            return ""

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        return f"[Target Mileage: {self.parent_log_entry.mileage}] " \
               f"{self.parent_log_entry.desc} " \
               f"[Type: {self.parent_log_entry.category}] [{self.parent_log_entry.id}]"

    def get_schedule_rule(self) -> str:
        return 'mileage'


@dataclass(order=True)
class ScheduledLogEntry(LogEntry):
    """LogEntry but scheduled in time based on date or target mileage and ability to be repeatable.
    \n
    Params:\n
    rule: str - should be equal to either 'date' or 'mileage' based on whether scheduled entry is scheduled every
    n days or every n mileage \n
    repeating: bool - whether this Scheduled Entry is re-added after completion and scheduled for a new date \n
    frequency: int - number of days or mileage increment between TODAY and Scheduled Entry \n
    \n
    If instance has 'date' arg not passed as empty string it will assume the entry is scheduled for one time only, if
    the passed date string is empty then it will automatically turn to today's date
    """

    frequency: int = 1
    repeating: bool = False
    _rule: str = 'date'
    _from_file: bool = False
    _schedule_obj: LogEntryScheduleRule = field(init=False, repr=False, default=None)

    def __post_init__(self):
        if self.date == "":
            self.date = TODAY

        self._count = 0

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, new: str):
        self._rule = new
        self._schedule_obj = self.create_schedule_rule_obj()

        if self._from_file:
            if self._count > 0:
                self.repeat()
            else:
                self._count += 1
        else:
            self.repeat()

    def filter_options(self) -> list[str]:
        return ['id', 'desc', 'date', 'component', 'category', 'mileage', 'frequency'] + list(self.custom_info.keys())

    def get_schedule_rule(self) -> str:
        return self._schedule_obj.get_schedule_rule()

    def create_schedule_rule_obj(self) -> LogEntryScheduleRule:
        new_obj = None

        match self.rule:
            case 'date': new_obj = DateScheduleRule(self.frequency, self)
            case 'mileage': new_obj = MileageScheduleRule(self.frequency, self)

        return new_obj

    def repeat(self):
        self.mileage = self.component.current_mileage
        self._schedule_obj.set_new_time()

    def get_new_date(self) -> int | str:
        return self._schedule_obj.get_new_time()

    def get_time_remaining(self) -> int | str:
        return self._schedule_obj.get_time_remaining()

    def time_remaining_to_str(self) -> str:
        return self._schedule_obj.time_remaining_to_str()

    def get_formatted_info(self) -> str:
        return self._schedule_obj.get_formatted_info()

    def __dict__(self) -> dict:
        d = {
                'desc': self.desc,
                'date': self.date,
                'mileage': self.mileage,
                'category': self.category.name,
                'tags': self.tags,
                'component': self.component.name,
                'id': self.id,
                'custom_info': self.custom_info,
                'rule': self.rule,
                'frequency': self.frequency,
                'repeating': self.repeating
            }
        return d

    def __hash__(self):
        return hash(self.id)
