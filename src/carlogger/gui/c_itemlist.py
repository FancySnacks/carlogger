from carlogger.items.item_sorter import ItemSorter


class ItemList:
    def __init__(self, items: list, parent, widget):
        self.items = items
        self.parent = parent
        self.widget = widget

    def sort_items(self, sort_method: str, reverse: bool = False) -> list:
        sorter = ItemSorter(self.items, sort_method)
        return sorter.get_sorted_list(reverse)

    def update_items(self, sort_key: str = '*', reverse: bool = False):
        if sort_key != "*":
            self.widget.update_items(self.sort_items(sort_key, reverse))

        self.widget.update_items(self.items)
