"""Filters log entries via key."""

import re

from uuid import UUID
from typing import Callable
from datetime import datetime

from carlogger.log_entry import LogEntry
from carlogger.util import is_date, format_date_string_to_tuple
from carlogger.entry_category import EntryCategory


class EntryFilter:
    """Filters log entries via key."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.filter_key = ''

    def arg_to_filter_func(self, arg: str) -> Callable:
        """Takes entry filter argument and returns a filter strategy pattern function."""
        self.filter_key = arg

        if arg == '*':
            return lambda entry: True

        if type(arg) == UUID:
            return self.filter_by_id

        if is_date(arg):
            return self.filter_by_date

        if is_date(arg[1::]) and arg[0] == "<":
            """Show entries older than specified date"""
            return self.filter_by_older_date

        if is_date(arg[1::]) and arg[0] == ">":
            """Show entries younger than specified date"""
            return self.filter_by_younger_date

        if arg in EntryCategory.get_categories():
            return self.filter_by_category

        if re.fullmatch(r'^>\d+', arg):
            """Show entries made at greater mileage than specified."""
            return self.filter_by_gt_mileage

        if re.fullmatch(r'^<\d+', arg):
            """Show entries made at lesser mileage than specified."""
            return self.filter_by_lt_mileage

        if arg[0] not in "<>" and arg.isnumeric() > -1:
            """Show entries made at mileage specified."""
            return self.filter_by_mileage

        return self.filter_by_desc

    def filter_by_id(self, entry: LogEntry) -> bool:
        return entry.id == self.filter_key

    def filter_by_desc(self, entry: LogEntry) -> bool:
        return entry.desc == self.filter_key

    def filter_by_date(self, entry: LogEntry) -> bool:
        return entry.date == self.filter_key

    def filter_by_older_date(self, entry: LogEntry) -> bool:
        d_gt = format_date_string_to_tuple(self.filter_key[1:])
        d_gt = datetime(day=d_gt[0], month=d_gt[1], year=d_gt[2])
        d_entry = format_date_string_to_tuple(entry.date)
        d_entry = datetime(day=d_entry[0], month=d_entry[1], year=d_entry[2])
        return d_entry < d_gt

    def filter_by_younger_date(self, entry: LogEntry) -> bool:
        d_lt = format_date_string_to_tuple(self.filter_key[1:])
        d_lt = datetime(day=d_lt[0], month=d_lt[1], year=d_lt[2])
        d_entry = format_date_string_to_tuple(entry.date)
        d_entry = datetime(day=d_entry[0], month=d_entry[1], year=d_entry[2])
        return d_entry > d_lt

    def filter_by_category(self, entry: LogEntry) -> bool:
        return entry.category == self.filter_key

    def filter_by_mileage(self, entry: LogEntry) -> bool:
        return entry.mileage == self.filter_key

    def filter_by_gt_mileage(self, entry: LogEntry) -> bool:
        return entry.mileage > int(self.filter_key[1::])

    def filter_by_lt_mileage(self, entry: LogEntry) -> bool:
        return entry.mileage < int(self.filter_key[1::])

    def get_filter_methods(self, filter_args: list[str]) -> list[Callable]:
        """Return a list of filter functions based on passed arguments."""
        if 'id' in filter_args:
            return [lambda entry: True]

        if '*' in filter_args:
            return [self.filter_by_id]

        return [self.arg_to_filter_func(arg) for arg in filter_args]

    def remove_conflicting_filters(self, filter_funcs: list[Callable]) -> list[Callable]:
        pass

    def apply_filters_to_entry_list(self, entry_list: list[LogEntry], filters: list[Callable]) -> list[LogEntry]:
        """Apply list of filter functions to a list of entries. Returns filtered list of entries."""
        filtered_entries = []
        [filtered_entries.extend(list(filter(fn, entry_list))) for fn in filters]
        return filtered_entries
