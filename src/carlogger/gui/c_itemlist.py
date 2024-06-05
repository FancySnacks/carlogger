from carlogger.items.item_sorter import ItemSorter


class ItemList:
    def __init__(self, parent, widget, app_session):
        self.items = []
        self.parent = parent
        self.widget = widget
        self.app_session = app_session

    def sort_items(self, items, sort_method: str, reverse: bool = False) -> list:
        item_sorter = ItemSorter(items, '')
        item_sorter.sort_method = sort_method
        return item_sorter.get_sorted_list(reverse)

    def create_items(self, items: list, header: str, sort_key: str = '*'):
        items = self.sort_items(items,
                                'latest' if sort_key == '*' else sort_key)
        self.items.append(items)
        self.widget.create_items(items, header, self._get_sort_methods(items))

    def update_items(self, index: int, sort_key: str = '*', reverse: bool = False):
        if sort_key != "*":
            self.widget.update_items(self.sort_items(self.items[index], sort_key, reverse), index)
        else:
            self.widget.update_items(self.items[index], index)

    def request_item_update(self):
        self.app_session.request_item_update()

    def collapse_widget(self):
        self.widget.collapse_widget()

    def _get_sort_methods(self, items) -> list[str]:
        class_attrib: list[str] = items[0].filter_options()
        return self._move_id_sort_button_to_front(class_attrib)

    def _move_id_sort_button_to_front(self, sort_funcs: list[str]) -> list[str]:
        for index, identifier in enumerate(sort_funcs):
            if identifier in ['name', 'id']:
                id_func_index = sort_funcs.index(identifier)
                sort_funcs.insert(0, sort_funcs.pop(id_func_index))

        return sort_funcs
