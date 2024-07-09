from customtkinter import CTkFrame

from carlogger.gui.c_itemlist import ItemList
from carlogger.gui.w_genericlist import Container
from carlogger.gui.w_collectionlist import CollectionContainer
from carlogger.gui.w_componentlist import ComponentContainer
from carlogger.gui.w_item_infobox import ItemInfoBox
from carlogger.gui.w_itemlist import ItemContainer


class ItemPage:
    def __init__(self, master, root, item_ref, go_to_func, add_widget_func, container=Container):
        self.item_ref = item_ref

        self.main_frame = CTkFrame(master)
        self.main_frame.grid(row=0, column=0, sticky='nsew')

        self.item_info_box = ItemInfoBox(self.main_frame, item_ref)

        self.container = container(self.main_frame,
                                   root=root,
                                   go_to_func=go_to_func,
                                   add_widget_func=add_widget_func)

    def create_items(self, items: list):
        self.container.create_items(items)

    def destroy(self):
        self.main_frame.destroy()


class CarPage(ItemPage):
    def __init__(self, master, root, item_ref, go_to_func, add_widget_func, container=CollectionContainer):
        super().__init__(master, root, item_ref, go_to_func, add_widget_func, container)


class CollectionPage(ItemPage):
    def __init__(self, master, root, item_ref, go_to_func, add_widget_func, container=ComponentContainer):
        super().__init__(master, root, item_ref, go_to_func, add_widget_func, container)


class ComponentPage:
    def __init__(self, master, root, item_ref):
        self.item_ref = item_ref

        self.main_frame = CTkFrame(master)
        self.main_frame.grid(row=0, column=0, sticky='nsew')

        self.item_info_box = ItemInfoBox(self.main_frame, item_ref)

        self.item_container = ItemContainer(self.main_frame, parent_car=None, root=root, component=self.item_ref)
        self.item_container.grid(row=1, column=0, sticky="nsew")

        self.item_list = ItemList(self.main_frame, widget=self.item_container, app_session=root.app_session)

    def destroy(self):
        self.main_frame.destroy()
