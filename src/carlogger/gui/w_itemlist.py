from customtkinter import CTkFrame, CTkButton, CTkLabel

from carlogger.gui.c_itemlist import ItemList


class ItemContainer(CTkFrame):
    def __init__(self, master, **values):
        super().__init__(master, **values)
        self.parent: ItemList = ...

        self.sort_buttons: list[SortButton] = []
        self._children_buttons: list = []

        self.buttons_frame = CTkFrame(master=self, height=35, fg_color="cyan")
        self.buttons_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.item_frame = CTkFrame(master=self, fg_color="aqua")
        self.item_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.add_sort_button('name')

    def sort_items(self, sort_key: str, reverse: bool):
        self.parent.update_items(sort_key, reverse)
        self.master.update_idletasks()

    def add_sort_button(self, sort_method: str, **kwargs):
        if not self.is_sort_method_already_used(sort_method):

            if len(self._children_buttons) % 2 != 0:
                self.add_separator()

            new_button = SortButton(master=self.buttons_frame,
                                    parent=self,
                                    sort_method=sort_method,
                                    column=len(self._children_buttons),
                                    **kwargs)
            self.sort_buttons.append(new_button)

            self._children_buttons.append(new_button)

    def add_separator(self):
        separator = CTkLabel(self.buttons_frame, text='|', font=('Lato', 25), text_color='white')
        separator.grid(row=0,
                       column=len(self._children_buttons))
        self._children_buttons.append(separator)

    def is_sort_method_already_used(self, sort_method: str) -> bool:
        items = [button.sort_method for button in self.sort_buttons]
        return sort_method in items

    def update_items(self, items: list):
        self.clear_items()

        c = 0
        for item in items:
            i = CTkLabel(self.item_frame, text=item.name, font=('Lato', 17))
            i.grid(row=c, column=0)
            c += 1

    def clear_items(self):
        for child in self.item_frame.winfo_children():
            child.destroy()


class SortButton(CTkButton):
    def __init__(self, master, parent, sort_method: str = 'SortOption', column: int = 0, **kwargs):
        super().__init__(master,
                         text=sort_method.upper(),
                         width=100,
                         height=30,
                         font=('Lato', 17),
                         command=self.call_sort_method,
                         **kwargs)

        self.sort_method = sort_method
        self.parent = parent
        self.reverse = True

        self.grid(row=0, column=column, padx=5, pady=5)

    def call_sort_method(self):
        self.reverse = not self.reverse
        self.format_button_text()
        self.parent.sort_items(self.sort_method, reverse=self.reverse)

    def format_button_text(self):
        self.text = f"{self.sort_method.upper()}{'v' if self.reverse else '^'}"
