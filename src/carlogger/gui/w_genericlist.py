from customtkinter import CTkFrame, CTkButton, CTkLabel

from abc import ABC
from typing import Callable

from carlogger.const import ITEM

from carlogger.gui.const_gui import get_img_from_path, collection_icon


class ContainerItem(ABC):
    image = collection_icon

    def __init__(self, master, item_ref: ITEM, column: int, row=0, **kwargs):
        self.master = master
        self.item_ref = item_ref

        self.column = column
        self.row = row

        # ===== Widget ===== #

        self.inner_frame = CTkFrame(self.master,
                                    fg_color='gray')
        self.inner_frame.grid(row=self.row, column=self.column, padx=5, pady=5)

        self.name = CTkLabel(self.inner_frame, text=self.item_ref.name, font=('Lato', 15))

        self.name.grid(row=0, column=0)

        self.button = CTkButton(self.inner_frame,
                                fg_color='transparent',
                                bg_color='gray',
                                hover_color='lightgray',
                                width=250,
                                height=175,
                                text='',
                                image=self.get_item_image(),
                                command=self.go_to)
        self.button.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    def get_item_image(self):
        if img := self.item_ref.custom_info.get('image'):
            return get_img_from_path(img, self)
        else:
            return self.image

    def go_to(self):
        self.master.go_to(self.item_ref)


class DummyContainerItem(ABC):
    def __init__(self, master, item_ref: ITEM, column: int, row=0, **kwargs):
        self.master = master
        self.item_ref = item_ref

        self.column = column
        self.row = row

        # ===== Widget ===== #

        self.inner_frame = CTkFrame(self.master,
                                    fg_color='transparent')
        self.inner_frame.grid(row=self.row, column=self.column, padx=5, pady=5)

        self.button = CTkButton(self.inner_frame,
                                fg_color='#323131',
                                border_color='lightgray',
                                border_width=3,
                                border_spacing=5,
                                hover_color='lightgray',
                                width=250,
                                height=210,
                                text='+',
                                font=('Lato', 50),
                                command=self.open_add_menu)
        self.button.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def open_add_menu(self):
        self.master.open_add_widget()


class Container(CTkFrame, ABC):
    image = collection_icon

    def __init__(self, master, root, go_to_func: Callable, add_widget_func: Callable, item_page_ref=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.root = root
        self.item_page_ref = item_page_ref
        self.go_to_func = go_to_func
        self.add_widget_func = add_widget_func
        self.widget_items = []

        self.grid(row=1, column=0, sticky='nsew')
        self.configure(fg_color='transparent')

        row = self._get_row() + 1
        column = len(self.widget_items) % 7
        new_item = DummyContainerItem(self, None, column, row=row)
        self.widget_items.append(new_item)

    def _get_row(self) -> int:
        return len(self.widget_items) // 7

    def add_item(self, item_ref: ITEM, widget_item_class=ContainerItem):
        row = self._get_row() + 1
        column = len(self.widget_items) % 7
        new_item = widget_item_class(self, item_ref, column, row=row)
        self.widget_items.append(new_item)

    def create_items(self, items: list[ITEM]):
        for item in items:
            self.add_item(item)

    def go_to(self, item_ref: ITEM):
        self.go_to_func(item_ref)

    def open_add_widget(self):
        self.add_widget_func()
