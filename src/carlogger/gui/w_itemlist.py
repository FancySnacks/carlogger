from customtkinter import CTkFrame, CTkButton, CTkLabel


class ItemContainer(CTkFrame):
    def __init__(self, master, **values):
        super().__init__(master, **values)
        self.sort_buttons: list[SortButton] = []
        self._children_buttons: list = []

        self.buttons_frame = CTkFrame(master=self, height=35, fg_color="cyan")
        self.buttons_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.item_frame = CTkFrame(master=self, fg_color="aqua")
        self.item_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.add_sort_button('name')
        self.add_sort_button('date')

    def sort_items(self):
        print('sort time')

    def add_sort_button(self, sort_method: str, **kwargs):
        if not self.is_sort_method_already_used(sort_method):

            if len(self._children_buttons) % 2 != 0:
                self.add_separator()

            new_button = SortButton(master=self.buttons_frame,
                                    sort_method=sort_method,
                                    column=len(self._children_buttons),
                                    command=self.sort_items,
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


class SortButton(CTkButton):
    def __init__(self, master, sort_method: str = 'SortOption', column: int = 0, **kwargs):
        super().__init__(master,
                         text=sort_method,
                         width=100,
                         height=30,
                         font=('Lato', 17),
                         **kwargs)

        self.sort_method = sort_method

        self.grid(row=0, column=column, padx=5, pady=5)
