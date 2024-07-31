"""Sorts list of items via key or criterion"""

import uuid
from typing import Callable, Any

from carlogger.items.log_entry import LogEntry, ScheduledLogEntry
from carlogger.util import date_string_to_date


class ItemSorter:
    def __init__(self, items: list, sort_method: str):
        self.items = items
        self.sort_method = sort_method

        self.sort_method_map = {'latest': self.sort_by_latest_entry,
                                'oldest': self.sort_by_oldest_entry,
                                'time_remaining': self.sort_by_time_remaining,
                                'car': self.sort_by_parent_car}

    def get_sorted_list(self, reverse_order: bool = False) -> list:
        sort_method: str | Callable = self._get_sort_method()

        if type(sort_method) != str:
            return sort_method(self.items, reverse_order)
        else:
            return self.sort_by_attrib(self.items, sort_method, reverse_order)

    def _get_sort_method(self) -> Callable:
        method: Callable = self.sort_method_map.get(self.sort_method, self.sort_method)
        return method

    def sort_by_attrib(self, items: list, attrib_name: str, reverse_order=False) -> list:
        items = self._filter_item_list_via_custom_attrib(items, attrib_name)
        return sorted(items, key=lambda item: self._attrib_sort(item, attrib_name), reverse=reverse_order)

    def _attrib_sort(self, item, attrib_name: str):
        try:
            return self._clamp_attrib(item, attrib_name)
        except AttributeError:
            return item.custom_info.get(attrib_name, None)

    def _clamp_attrib(self, item, attrib_name: str) -> Any:
        if attrib_name == 'date':
            return date_string_to_date(getattr(item, 'date'))

        if attrib_name == 'id':
            return uuid.UUID(hex=getattr(item, 'id'))

        atb = getattr(item, attrib_name)

        if type(atb) not in (int, float, str):
            return str(atb)
        else:
            return atb

    def _filter_item_list_via_custom_attrib(self, items, attrib) -> list:
        return list(filter(lambda item: self._attrib_exists(item, attrib), items))

    def _attrib_exists(self, item, attrib) -> bool:
        try:
            getattr(item, attrib)
            return True
        except AttributeError:
            if item.custom_info.get(attrib):
                return True
            else:
                return False

    def sort_by_time_remaining(self, items: list, reversed=False):
        if items[0].__class__.__name__ in ('LogEntry', 'ScheduledLogEntry'):
            return self.sort_by_time_remaining_raw(items)

        entry_map: list[tuple[Any, list]] = []

        for item in items:
            entry_map.append((item, [entry.get_time_remaining() for entry in item.get_all_entry_logs()]))

        items = sorted(entry_map, key=lambda x: x[1], reverse=reversed)

        return [e[0] for e in items]

    def sort_by_time_remaining_raw(self, items: list[LogEntry | ScheduledLogEntry], reversed=False) -> list:
        entry_map: list[tuple] = []

        for item in items:
            entry_map.append((item, item.get_time_remaining()))

        items = sorted(entry_map, key=lambda x: x[1], reverse=reversed)

        return [e[0] for e in items]

    def sort_by_latest_entry(self, items: list, *args) -> list:
        if items[0].__class__.__name__ in ('LogEntry', 'ScheduledLogEntry'):
            return self.sort_by_latest_entry_raw(items)

        entry_map: list[tuple[Any, ...]] = []

        for item in items:
            entry_map.append((item, date_string_to_date(item.latest_entry.date)))

        items = sorted(entry_map, key=lambda x: x[1], reverse=True)

        return [e[0] for e in items]

    def sort_by_oldest_entry(self, items: list, *args) -> list:
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

    def sort_by_parent_car(self, items: list[LogEntry | ScheduledLogEntry], reverse_order=False):
        entries: list[tuple[str, LogEntry | ScheduledLogEntry]] = []

        for entry in items:
            parent_car = entry.component.parent.car.car_info.name
            entries.append((parent_car, entry))

        sorted_entries = sorted(entries, key=lambda x: x[0], reverse=reverse_order)
        return [entry[1] for entry in sorted_entries]
