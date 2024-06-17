from customtkinter import CTkFrame

from carlogger.gui.c_itemlist import ItemList
from carlogger.gui.w_itemlist import ItemContainer


class Homepage(CTkFrame):
    def __init__(self, master, root, **kwargs):
        super().__init__(master,
                         corner_radius=0,
                         fg_color="transparent",
                         **kwargs)
        self.master = master
        self.root = root

        self.grid(row=0, column=0, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.item_container = ItemContainer(self, parent_car=None, root=self.root)
        self.item_container.grid(row=1, column=0, sticky="nsew")

        self.item_list = self.item_list = ItemList(self,
                                                   widget=self.item_container,
                                                   app_session=self.root.app_session)

    def create_items(self, items, parent_car, header, sort_key: str = '*'):
        self.item_container.parent = self.item_list
        self.item_container.parent_car = parent_car
        self.item_container.app_session = self.root.app_session
        self.item_list.create_items(items, header, sort_key)
