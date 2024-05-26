from carlogger.items.item_sorter import ItemSorter
from carlogger.util import get_all_class_properties


class ItemList:
    def __init__(self, items: list, item_class, parent, widget):
        self.items = items
        self.item_class = item_class
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
        class_attrib = get_all_class_properties(self.item_class)
        funcs = self.item_sorter.sort_method_map.keys()
        joined_lists = list(class_attrib) + list(funcs)
        return self._move_id_sort_button_to_front(joined_lists)

    def _move_id_sort_button_to_front(self, sort_funcs: list[str]) -> list[str]:
        for index, identifier in enumerate(sort_funcs):
            if identifier in ['name', 'id']:
                id_func_index = sort_funcs.index(identifier)
                sort_funcs.insert(0, sort_funcs.pop(id_func_index))

        return sort_funcs
