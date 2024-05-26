from customtkinter import CTkFrame, CTkButton, CTkLabel

from carlogger.gui.c_itemlist import ItemList


class ItemContainer(CTkFrame):
    def __init__(self, master, **values):
        super().__init__(master, **values)
        self.parent: ItemList = ...

        self.item_list_widgets: list[SortableItemList] = []

    def create_items(self, items: list, header: str, filter_opts: list[str]):
        new_sortable_item_list = SortableItemList(self, self, header, items, len(self.item_list_widgets))
        self.item_list_widgets.append(new_sortable_item_list)
        self.add_sort_buttons(filter_opts, new_sortable_item_list)

    def update_items(self, items: list, index: int):
        sortable_item_list = self.item_list_widgets[index]
        sortable_item_list.update_items(items)

    def add_sort_buttons(self, sort_methods: list[str], item_list):
        for s in sort_methods:
            item_list.add_sort_button(s)


class SortableItemList(CTkFrame):
    def __init__(self, master, parent: ItemContainer, header: str, items: list, index: int, **values):
        super().__init__(master, **values)
        self.parent: ItemContainer = parent
        self.header = header
        self.index = index

        self.sort_buttons: list[SortButton] = []
        self.active_sort_button: SortButton = None
        self._children_buttons: list = []

        self.items: list[Item] = items

        # ===== Widgets ==== #

        self.item_label = CTkLabel(self.parent, text=header, font=('Lato', 20), anchor='w')
        self.item_label.pack(expand=True, fill='x', padx=10, pady=5)

        self.buttons_frame = CTkFrame(master=self.parent, height=35, fg_color="cyan")
        self.buttons_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.item_frame = CTkFrame(master=self.parent, fg_color="skyblue")
        self.item_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.update_items(self.items)

    def sort_items(self, sort_key: str, button_ref, reverse: bool):
        if self.active_sort_button and self.active_sort_button != button_ref:
            self.active_sort_button.unfocus()
        self.active_sort_button = button_ref

        self.parent.parent.update_items(self.index, sort_key, reverse)
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

        c = 0
        for item in items:
            new_item = self.create_item(self.item_frame, item, row=-1)
            self.items.append(new_item)
            c += 1

    def create_item(self, master, item_obj, row=-1):
        if row == -1:
            row = len(self.items)

        new_item = Item(master=master,
                        parent=self,
                        item_ref=item_obj,
                        row=row)

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
    def __init__(self, master, parent: SortableItemList, item_ref, row: int = 0, scheduled=False, **kwargs):
        super().__init__(master,
                         height=100,
                         fg_color='blue',
                         corner_radius=0,
                         **kwargs)
        self.parent = parent
        self.scheduled = scheduled
        self.id = row
        self.item_ref = item_ref

        # ===== Widget ===== #

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

        for index, item in enumerate(self.item_ref.custom_info.items()):
            self.new_label = CTkLabel(self,
                                      text=item[1],
                                      font=('Lato', 17),
                                      width=150,
                                      justify='left',
                                      anchor='w')
            self.new_label.grid(row=0, column=index + 4, padx=5, pady=2)

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
