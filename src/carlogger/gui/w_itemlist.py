from customtkinter import CTkFrame, CTkButton, CTkLabel

from carlogger.gui.c_itemlist import ItemList


class ItemContainer(CTkFrame):
    def __init__(self, master, **values):
        super().__init__(master, **values)
        self.parent: ItemList = ...

        self.sort_buttons: list[SortButton] = []
        self.active_sort_button: SortButton = None
        self._children_buttons: list = []

        self.items: list[Item] = []
        self.scheduled_items: list[Item] = []

        # ===== Widgets ==== #

        self.buttons_frame = CTkFrame(master=self, height=35, fg_color="cyan")
        self.buttons_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.scheduled_item_label = CTkLabel(self, text='Scheduled Log Entries', font=('Lato', 20), anchor='w')
        self.scheduled_item_label.pack(expand=True, fill='x', padx=10, pady=5)

        self.scheduled_item_frame = CTkFrame(master=self, fg_color="skyblue")
        self.scheduled_item_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.item_label = CTkLabel(self, text='Log Entries', font=('Lato', 20), anchor='w')
        self.item_label.pack(expand=True, fill='x', padx=10, pady=5)

        self.item_frame = CTkFrame(master=self, fg_color="turquoise")
        self.item_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.add_sort_button('name')

    def sort_items(self, sort_key: str, button_ref, reverse: bool):
        if self.active_sort_button and self.active_sort_button != button_ref:
            self.active_sort_button.unfocus()
        self.active_sort_button = button_ref

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
        self.items = []
        self.scheduled_items = []

        for item in items:
            match item.__class__.__name__:
                case 'ScheduledLogEntry':
                    new_item = self.create_item(self.scheduled_item_frame, item, scheduled=True)
                    self.scheduled_items.append(new_item)
                case _:
                    new_item = self.create_item(self.item_frame, item)
                    self.items.append(new_item)

    def create_item(self, master, item_obj, scheduled=False):
        new_item = Item(master=master,
                        parent=self,
                        item_ref=item_obj,
                        row=len(self.items),
                        scheduled=scheduled)

        return new_item

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
        self.parent.sort_items(self.sort_method, self, reverse=self.reverse)

    def format_button_text(self):
        self.configure(text=f"{self.sort_method.upper()} {'v' if self.reverse else '^'}")

    def unfocus(self):
        self.configure(text=self.sort_method.upper())


class Item(CTkFrame):
    def __init__(self, master, parent: ItemContainer, item_ref, row: int = 0, scheduled=False, **kwargs):
        super().__init__(master,
                         height=100,
                         fg_color='blue',
                         corner_radius=0,
                         **kwargs)
        self.parent = parent
        self.scheduled = scheduled
        self.id = row
        self.item_ref = item_ref

        self.grid(row=row, column=0, sticky="we", padx=2, pady=2)

        self.date_label = CTkLabel(self, text=self._get_time_remaining(), font=('Lato', 17), width=100)
        self.date_label.grid(row=0, column=0, padx=5, pady=2)

        self.desc_label = CTkLabel(self,
                                   text=self._get_item_name(),
                                   font=('Lato', 17),
                                   wraplength=300,
                                   width=315,
                                   justify='left',
                                   anchor='w')
        self.desc_label.grid(row=0, column=1, padx=5, pady=2)

        self.category_label = CTkLabel(self, text=self.item_ref.category.capitalize(), font=('Lato', 17), width=100)
        self.category_label.grid(row=0, column=2, padx=5, pady=2)

        self.mileage_label = CTkLabel(self,
                                      text=self._get_mileage_remaining(),
                                      font=('Lato', 17),
                                      width=150,
                                      justify='left',
                                      anchor='w')
        self.mileage_label.grid(row=0, column=3, padx=5, pady=2)

    def _get_item_name(self) -> str:
        properties = self.item_ref.to_json().get('name', ''), self.item_ref.to_json().get('desc', ''), ''

        return sorted(properties, reverse=True)[0]

    def _get_time_remaining(self) -> str:
        if self.scheduled and self.item_ref.get_schedule_rule() == 'date':
            return f"{self.item_ref.date}\n" \
                   f"({self.item_ref.time_remaining_to_str()})"

        return self.item_ref.date

    def _get_mileage_remaining(self):
        if self.scheduled and self.item_ref.get_schedule_rule() == 'mileage':
            return f"{self.item_ref.mileage} km\n" \
                   f"(in {abs(self.item_ref.get_time_remaining())} km)"

        return f"{self.item_ref.mileage} km"
