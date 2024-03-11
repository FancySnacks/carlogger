"""Filters log entries via key."""

import re

from uuid import UUID
from typing import Callable, Optional
from datetime import datetime

from carlogger.log_entry import LogEntry
from carlogger.util import is_date, format_date_string_to_tuple
from carlogger.entry_category import EntryCategory


class CountFilter:
    def __init__(self, count: int):
        self.count = count

    def return_n_entries(self, entry_list: list[LogEntry]) -> list[LogEntry]:
        if self.count < 0:
            return entry_list[:self.count:]

        if self.count == 0:
            return []

        return entry_list[self.count::]


class FilterWorker:
    def __init__(self, key: str, filter_method: Callable[[LogEntry, str], bool], filter_group: str):
        self.key = key
        self.filter_method = filter_method
        self.filter_group = filter_group

    def apply_filter(self, entries: list[LogEntry]) -> list[LogEntry]:
        filtered_entries = []

        for entry in entries:
            if self.filter_method(entry, self.key):
                filtered_entries.append(entry)

        return filtered_entries

    def __repr__(self) -> str:
        return self.filter_method.__name__


class EntryFilter:
    """Filters log entries via key."""
    def __init__(self):
        self.filters: list[FilterWorker] = []
        self.active_filter_groups: list[str] = []
        self.count_filter: Optional[CountFilter] = None

        self.filter_dict = {"*": (self.filter_all, 'all'),
                            "id": (self.filter_by_desc, 'all'),
                            "desc": (self.filter_by_desc, 'desc'),
                            "category": (self.filter_by_desc, 'category'),
                            "date": (self.filter_by_date, 'date'),
                            "date_older": (self.filter_by_older_date, 'date'),
                            "date_younger": (self.filter_by_younger_date, 'date'),
                            "mileage": (self.filter_by_date, 'date'),
                            "mileage_gt": (self.filter_by_gt_mileage, 'mileage'),
                            "mileage_lt": (self.filter_by_lt_mileage, 'mileage'),
                            }

    def apply_filters_to_entry_list(self, args: list[str], entry_list: list[LogEntry]) -> list[LogEntry]:
        """Apply list of filter functions to a list of entries. Returns filtered list of entries."""
        args = self._create_count_filter(args)

        self._create_filter_group_from_args(args)

        filtered_entries = []

        for filter in self.filters:
            filtered_entries = filter.apply_filter(entry_list)

        if self.count_filter:
            return self.count_filter.return_n_entries(filtered_entries)

        return filtered_entries

    def _create_count_filter(self, args: list[str]) -> list[str]:
        cpattern = re.compile(r'^-*\d+$')
        matches = [arg for arg in args if re.search(cpattern, arg)]

        if matches:
            self.count_filter = CountFilter(int(matches[0]))
            args.remove(matches[0])

        return args

    def _create_filter_group_from_args(self, args: list[str]):
        """Turn command line arguments into list of filters."""
        for arg in args:
            filterclass = self._create_filter_class_from_arg(arg)
            self._add_filter(filterclass)

    def _create_filter_class_from_arg(self, arg: str) -> FilterWorker:
        """Takes entry filter argument and returns a filter strategy pattern function."""

        if arg == '*':
            return FilterWorker(arg, *self.filter_dict['*'])

        if type(arg) == UUID:
            return FilterWorker(arg, *self.filter_dict['id'])

        if is_date(arg):
            return FilterWorker(arg, *self.filter_dict['date'])

        if is_date(arg[1::]) and arg[0] == "<":
            """Show entries older than specified date"""
            return FilterWorker(arg, *self.filter_dict['date_older'])

        if is_date(arg[1::]) and arg[0] == ">":
            """Show entries younger than specified date"""
            return FilterWorker(arg, *self.filter_dict['date_younger'])

        if arg in EntryCategory.get_categories():
            return FilterWorker(arg, *self.filter_dict['category'])

        if re.fullmatch(r'^>\d+', arg):
            """Show entries made at greater mileage than specified."""
            return FilterWorker(arg, *self.filter_dict['mileage_gt'])

        if re.fullmatch(r'^<\d+', arg):
            """Show entries made at lesser mileage than specified."""
            return FilterWorker(arg, *self.filter_dict['mileage_lt'])

        return FilterWorker(arg, *self.filter_dict['desc'])
    
    def _add_filter(self, filterclass: FilterWorker):
        """Add filter to list of filters, ensuring that no duplicate filters get added."""
        if filterclass.filter_group in self.active_filter_groups:
            return
        
        if 'all' in self.active_filter_groups:
            return
        
        self.filters.append(filterclass)
        self.active_filter_groups.append(filterclass.filter_group)

    def filter_all(self, entry: LogEntry, filter_key: str) -> bool:
        return True

    def filter_by_id(self, entry: LogEntry, filter_key: str) -> bool:
        return entry.id == filter_key

    def filter_by_desc(self, entry: LogEntry, filter_key: str) -> bool:
        return entry.desc == filter_key

    def filter_by_date(self, entry: LogEntry, filter_key: str) -> bool:
        return entry.date == filter_key

    def filter_by_older_date(self, entry: LogEntry, filter_key: str) -> bool:
        d_gt = format_date_string_to_tuple(filter_key[1:])
        d_gt = datetime(day=d_gt[0], month=d_gt[1], year=d_gt[2])
        d_entry = format_date_string_to_tuple(entry.date)
        d_entry = datetime(day=d_entry[0], month=d_entry[1], year=d_entry[2])
        return d_entry < d_gt

    def filter_by_younger_date(self, entry: LogEntry, filter_key: str) -> bool:
        d_lt = format_date_string_to_tuple(filter_key[1:])
        d_lt = datetime(day=d_lt[0], month=d_lt[1], year=d_lt[2])
        d_entry = format_date_string_to_tuple(entry.date)
        d_entry = datetime(day=d_entry[0], month=d_entry[1], year=d_entry[2])
        return d_entry > d_lt

    def filter_by_category(self, entry: LogEntry, filter_key: str) -> bool:
        return entry.category == filter_key

    def filter_by_gt_mileage(self, entry: LogEntry, filter_key: str) -> bool:
        return entry.mileage > int(filter_key[1::])

    def filter_by_lt_mileage(self, entry: LogEntry, filter_key: str) -> bool:
        return entry.mileage < int(filter_key[1::])
