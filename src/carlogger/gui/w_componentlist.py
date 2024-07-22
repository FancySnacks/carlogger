from customtkinter import CTkFrame, CTkButton

from carlogger.gui.w_deletion_confirmation import DeletionConfirmation
from carlogger.gui.w_genericlist import Container, ContainerItem

from carlogger.gui.const_gui import component_icon

from carlogger.const import ITEM


class ComponentItem(ContainerItem):
    image = component_icon


class ComponentContainer(Container):
    def __init__(self, master, root, go_to_func, add_widget_func, item_page_ref, **kwargs):
        super().__init__(master, root, go_to_func, add_widget_func, item_page_ref, **kwargs)

        self.management_buttons_frame = CTkFrame(self, fg_color='transparent')
        self.management_buttons_frame.grid(row=0, column=0, sticky='ew', pady=10)

        self.edit_button = CTkButton(self.management_buttons_frame,
                                     text="Edit Collection",
                                     font=('Lato', 18),
                                     fg_color='green',
                                     width=35,
                                     corner_radius=0,
                                     command=self.open_edit_window)
        self.edit_button.grid(row=0, column=0, sticky='w', padx=5)

        self.del_button = CTkButton(self.management_buttons_frame,
                                    text="Delete Collection",
                                    font=('Lato', 18),
                                    fg_color='red',
                                    width=35,
                                    corner_radius=0,
                                    command=self.attempt_delete)
        self.del_button.grid(row=0, column=1, sticky='w', padx=5)

    def add_item(self, item_ref: ITEM, widget_item_class=ComponentItem):
        super().add_item(item_ref, widget_item_class)

    def attempt_delete(self):
        if len(self.item_page_ref.item_ref.children) > 0:
            DeletionConfirmation(self.master, self.root, self.item_page_ref.item_ref, self.delete_collection)
        else:
            self.delete_collection()

    def delete_collection(self):
        parent_car_name = self.item_page_ref.item_ref.car.name
        coll_to_del_name = self.item_page_ref.item_ref.name
        self.root.app_session.delete_collection(parent_car_name, coll_to_del_name)

        self.root.navigation.go_back()

    def open_edit_window(self):
        self.root.open_collection_edit_window()
