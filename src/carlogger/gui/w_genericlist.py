from customtkinter import CTkFrame, CTkButton, CTkLabel

from abc import ABC
from typing import Callable

from carlogger.const import ITEM


class ContainerItem(ABC):
    def __init__(self, master, item_ref: ITEM, column: int, row=0, **kwargs):
        self.master = master
        self.item_ref = item_ref

        self.column = column
        self.row = row

        # ===== Widget ===== #

        self.inner_frame = CTkFrame(self.master,
                                    fg_color='gray')
        self.inner_frame.grid(row=self.row, column=self.column, padx=5, pady=5)

        self.name = CTkLabel(self.inner_frame,
                             text=self.item_ref.name,)

        self.name.grid(row=0, column=0)

        self.button = CTkButton(self.inner_frame,
                                fg_color='transparent',
                                bg_color='gray',
                                hover_color='lightgray',
                                width=250,
                                height=175,
                                text='',
                                command=self.go_to)
        self.button.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    def go_to(self):
        self.master.go_to(self.item_ref)


class Container(CTkFrame, ABC):
    def __init__(self, master, root, go_to_func: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.root = root
        self.go_to_func = go_to_func
        self.widget_items = []

        self.grid(row=0, column=0, sticky='nsew')

    def add_item(self, item_ref: ITEM, widget_item_class=ContainerItem):
        row = len(self.widget_items) // 7
        column = len(self.widget_items) % 7
        new_item = widget_item_class(self, item_ref, column, row=row)
        self.widget_items.append(new_item)

    def create_items(self, items: list[ITEM]):
        for item in items:
            self.add_item(item)

    def go_to(self, item_ref: ITEM):
        self.go_to_func(item_ref)
