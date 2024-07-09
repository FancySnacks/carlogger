from customtkinter import CTkFrame, CTkButton

from carlogger.gui.w_genericlist import Container, ContainerItem
from carlogger.const import ITEM


class CollectionItem(ContainerItem):
    pass


class CollectionContainer(Container):
    def __init__(self, master, root, go_to_func, add_widget_func):
        super().__init__(master, root, go_to_func, add_widget_func)

        self.management_buttons_frame = CTkFrame(self, fg_color='transparent')
        self.management_buttons_frame.grid(row=0, column=0, sticky='ew')

        self.edit_button = CTkButton(self.management_buttons_frame,
                                     text="Edit Car",
                                     font=('Lato', 18),
                                     fg_color='green',
                                     width=35,
                                     corner_radius=0,
                                     command=self.open_edit_window)
        self.edit_button.grid(row=0, column=0, sticky='w', padx=5)

        self.del_button = CTkButton(self.management_buttons_frame,
                                    text="Delete Car",
                                    font=('Lato', 18),
                                    fg_color='red',
                                    width=35,
                                    corner_radius=0,
                                    command=NotImplemented)
        self.del_button.grid(row=0, column=1, sticky='w', padx=5)

    def add_item(self, item_ref: ITEM, widget_item_class=CollectionItem):
        super().add_item(item_ref)

    def open_edit_window(self):
        self.root.open_car_edit_window()
