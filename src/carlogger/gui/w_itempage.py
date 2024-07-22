from customtkinter import CTkFrame

from carlogger.gui.c_itemlist import ItemList
from carlogger.gui.w_genericlist import Container
from carlogger.gui.w_collectionlist import CollectionContainer
from carlogger.gui.w_componentlist import ComponentContainer
from carlogger.gui.w_item_infobox import ItemInfoBox, CollectionInfoBox, ComponentInfoBox
from carlogger.gui.w_itemlist import ItemContainer
from carlogger.gui.const_gui import component_icon


class ItemPage:
    def __init__(self, master, root, item_ref, go_to_func, add_widget_func, container=Container,
                 itembox_widget=ItemInfoBox):
        self.item_ref = item_ref
        self.itembox_widget = itembox_widget

        self.main_frame = CTkFrame(master)
        self.main_frame.grid(row=0, column=0, sticky='nsew')

        self.main_frame.grid_columnconfigure(0, weight=1)

        self.item_info_box = itembox_widget(self.main_frame, item_ref, image=container.image)

        self.container = container(self.main_frame,
                                   root=root,
                                   go_to_func=go_to_func,
                                   add_widget_func=add_widget_func,
                                   item_page_ref=self)

    def create_items(self, items: list):
        self.container.create_items(items)

    def destroy(self):
        self.main_frame.destroy()


class CarPage(ItemPage):
    def __init__(self, master, root, item_ref, go_to_func, add_widget_func, container=CollectionContainer,
                 itembox_widget=ItemInfoBox):
        super().__init__(master, root, item_ref, go_to_func, add_widget_func, container, itembox_widget)


class CollectionPage(ItemPage):
    def __init__(self, master, root, item_ref, go_to_func, add_widget_func, container=ComponentContainer,
                 itembox_widget=CollectionInfoBox):
        super().__init__(master, root, item_ref, go_to_func, add_widget_func, container, itembox_widget)


class ComponentPage:
    def __init__(self, master, root, item_ref, itembox_widget=ComponentInfoBox):
        self.item_ref = item_ref
        self.itembox_widget = itembox_widget

        self.main_frame = CTkFrame(master)
        self.main_frame.grid(row=0, column=0, sticky='nsew')

        self.main_frame.grid_columnconfigure(0, weight=1)

        self.item_info_box = self.itembox_widget(self.main_frame, item_ref, image=component_icon)

        self.item_container = ItemContainer(self.main_frame, parent_car=None, root=root, component=self.item_ref,
                                            item_page_ref=self)
        self.item_container.grid(row=1, column=0, sticky="nsew")

        self.item_list = ItemList(self.main_frame, widget=self.item_container, app_session=root.app_session)

    def destroy(self):
        self.main_frame.destroy()
