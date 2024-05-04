"""Sorts list of items via key or criterion"""

from typing import Callable


class ItemSorter:
    def __init__(self, items: list, sort_method: str):
        self.items = items
        self.sort_method = sort_method

        self.sort_method_map = {'latest': lambda x: x.entry}

    def get_sort_method(self) -> Callable:
        method: Callable = self.sort_method_map.get(self.sort_method, self.sort_method)
        return method

    def get_sorted_list(self, reverse_order: bool = False) -> list:
        method: str | Callable = self.get_sort_method()

        if type(method) == Callable:
            return method()
        else:
            return self.sort_by_attrib(self.items, method, reverse_order)

    def sort_by_attrib(self, items: list, attrib_name: str, reverse_order=False) -> list:
        return sorted(items, key=lambda item: getattr(item, attrib_name), reverse=reverse_order)

    def sort_by_latest_entry(self, items: list, reverse_order=False) -> list:
        """TODO"""
