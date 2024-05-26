"""Sorts list of items via key or criterion"""

from typing import Callable, Any

from carlogger.items.log_entry import LogEntry, ScheduledLogEntry
from carlogger.util import date_string_to_date


class ItemSorter:
    def __init__(self, items: list, sort_method: str):
        self.items = items
        self.sort_method = sort_method

        self.sort_method_map = {'latest': self.sort_by_latest_entry,
                                'oldest': self.sort_by_oldest_entry}

    def get_sorted_list(self, reverse_order: bool = False) -> list:
        sort_method: str | Callable = self._get_sort_method()

        if type(sort_method) != str:
            return sort_method(self.items)
        else:
            return self.sort_by_attrib(self.items, sort_method, reverse_order)

    def _get_sort_method(self) -> Callable:
        method: Callable = self.sort_method_map.get(self.sort_method, self.sort_method)
        return method

    def sort_by_attrib(self, items: list, attrib_name: str, reverse_order=False) -> list:
        return sorted(items, key=lambda item: self._attrib_sort(item, attrib_name), reverse=reverse_order)

    def _attrib_sort(self, item, attrib_name: str):
        try:
            return getattr(item, attrib_name)
        except AttributeError:
            return item.custom_info.get(attrib_name)

    def sort_by_latest_entry(self, items: list) -> list:
        if items[0].__class__.__name__ in ('LogEntry', 'ScheduledLogEntry'):
            return self.sort_by_latest_entry_raw(items)

        entry_map: list[tuple[Any, list]] = []

        for item in items:
            entry_map.append((item, [date_string_to_date(entry.date) for entry in item.get_all_entry_logs()]))

        items = sorted(entry_map, key=lambda x: x[1], reverse=True)

        return [e[0] for e in items]

    def sort_by_oldest_entry(self, items: list) -> list:
        if items[0].__class__.__name__ in ('LogEntry', 'ScheduledLogEntry'):
            return self.sort_by_oldest_entry_raw(items)

        entry_map: list[tuple[Any, list]] = []

        for item in items:
            entry_map.append((item, [date_string_to_date(entry.date) for entry in item.get_all_entry_logs()]))

        items = sorted(entry_map, key=lambda x: x[1])

        return [e[0] for e in items]

    def sort_by_latest_entry_raw(self, items: list[LogEntry | ScheduledLogEntry]) -> list:
        entry_map: list[tuple] = []

        for item in items:
            entry_map.append((item, date_string_to_date(item.date)))

        items = sorted(entry_map, key=lambda x: x[1], reverse=True)

        return [e[0] for e in items]

    def sort_by_oldest_entry_raw(self, items: list[LogEntry | ScheduledLogEntry]) -> list:
        entry_map: list[tuple] = []

        for item in items:
            entry_map.append((item, date_string_to_date(item.date)))

        items = sorted(entry_map, key=lambda x: x[1])

        return [e[0] for e in items]
