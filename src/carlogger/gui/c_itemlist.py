from carlogger.items.item_sorter import ItemSorter


class ItemList:
    def __init__(self, items: list, parent, widget):
        self.items = items
        self.parent = parent
        self.widget = widget
        self.item_sorter = ItemSorter(self.items, '')

    def sort_items(self, sort_method: str, reverse: bool = False) -> list:
        self.item_sorter.sort_method = sort_method
        return self.item_sorter.get_sorted_list(reverse)

    def update_items(self, sort_key: str = '*', reverse: bool = False):
        if sort_key != "*":
            self.widget.update_items(self.sort_items(sort_key, reverse))
        else:
            self.widget.update_items(self.items)

    def create_sort_buttons(self):
        for sort_method in self._get_sort_methods():
            self.widget.add_sort_button(sort_method)

    def _get_sort_methods(self) -> list[str]:
        return self.item_sorter.sort_method_map.keys()
