from customtkinter import CTkFrame

from carlogger.gui.c_itemlist import ItemList

from carlogger.const import ITEM


class CollectionContainer(CTkFrame):
    def __init__(self, master, root, parent: ItemList, items: list[ITEM], **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.root = root

        self.parent: ItemList = parent
        self.items: list[ITEM] = items
        self.widget_items = []

    def add_item(self, item_ref: ITEM):
        new_item = CollectionItem(self, item_ref)
        self.items.append(item_ref)
        self.widget_items.append(new_item)


class CollectionItem(CTkFrame):
    def __init__(self, master, item_ref: ITEM, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.item_ref = item_ref
