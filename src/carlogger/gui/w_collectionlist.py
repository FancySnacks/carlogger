from customtkinter import CTkFrame, CTkButton

from carlogger.gui.w_deletion_confirmation import DeletionConfirmation
from carlogger.gui.w_genericlist import Container, ContainerItem
from carlogger.gui.const_gui import collection_icon

from carlogger.const import ITEM


class CollectionItem(ContainerItem):
    image = collection_icon


class CollectionContainer(Container):
    def __init__(self, master, root, go_to_func, add_widget_func, item_page_ref, **kwargs):
        super().__init__(master, root, go_to_func, add_widget_func, item_page_ref, **kwargs)

        self.management_buttons_frame = CTkFrame(self, fg_color='transparent')
        self.management_buttons_frame.grid(row=0, column=0, sticky='ew')

        self.edit_button = CTkButton(self.management_buttons_frame,
                                     text="Edit Car",
                                     font=('Lato', 18),
                                     fg_color='green',
                                     width=35,
                                     corner_radius=0,
                                     command=self.open_edit_window)
        self.edit_button.grid(row=0, column=0, sticky='w', padx=5, pady=10)

        self.del_button = CTkButton(self.management_buttons_frame,
                                    text="Delete Car",
                                    font=('Lato', 18),
                                    fg_color='red',
                                    width=35,
                                    corner_radius=0,
                                    command=self.attempt_delete)
        self.del_button.grid(row=0, column=1, sticky='w', padx=5)

    def add_item(self, item_ref: ITEM, widget_item_class=CollectionItem):
        super().add_item(item_ref, widget_item_class)

    def attempt_delete(self):
        if len(self.item_page_ref.item_ref.children) > 0:
            DeletionConfirmation(self.master, self.root, self.item_page_ref.item_ref, self.delete_car)
        else:
            self.delete_car()

    def delete_car(self):
        car_name = self.item_page_ref.item_ref.name
        self.root.app_session.delete_car(car_name)

        self.root.navigation.go_back()

    def open_edit_window(self):
        self.root.open_car_edit_window()
