from __future__ import annotations

from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkCheckBox, BooleanVar

from typing import TYPE_CHECKING

from carlogger.gui.c_itemlist import ItemList
from carlogger.gui.w_deletion_confirmation import DeletionConfirmation
from carlogger.gui.const_gui import BG_GRAY_PRIMARY, BLUE_1

from carlogger.const import ITEM

if TYPE_CHECKING:
    from carlogger.gui.root_window import RootWindow


class ItemContainer(CTkFrame):
    def __init__(self, master, parent_car, root: RootWindow, homepage=False, item_page_ref=None, **values):
        super().__init__(master)
        self.root = root
        self.parent_car = parent_car
        self.homepage = homepage
        self.item_page_ref = item_page_ref

        self.parent: ItemList = ...
        self.app_session = ...
        self.component = values.get('component')

        self.item_list_widgets: list[SortableItemList] = []

        if not self.homepage:
            self.edit_button_frame = CTkFrame(self, fg_color='transparent')
            self.edit_button_frame.pack(anchor='w', pady=10)

            self.edit_button = CTkButton(self.edit_button_frame,
                                         text="Edit Component",
                                         font=('Lato', 18),
                                         width=35,
                                         corner_radius=0,
                                         command=self.open_edit_window)
            self.edit_button.grid(row=0, column=0, sticky='w', padx=5)

            self.del_button = CTkButton(self.edit_button_frame,
                                        text="Delete Component",
                                        font=('Lato', 18),
                                        fg_color='red',
                                        width=35,
                                        corner_radius=0,
                                        command=self.attempt_delete)
            self.del_button.grid(row=0, column=1, sticky='w', padx=5)

    def open_edit_window(self):
        self.root.open_component_edit_window()

    def attempt_delete(self):
        if len(self.item_page_ref.item_ref.children) > 0:
            DeletionConfirmation(self.master, self.root, self.item_page_ref.item_ref, self.delete_component)
        else:
            self.delete_component()

    def delete_component(self):
        parent_car_name = self.item_page_ref.item_ref.parent.car.name
        parent_coll_name = self.item_page_ref.item_ref.parent.name
        comp_to_del_name = self.item_page_ref.item_ref.name
        self.root.app_session.delete_component(parent_car_name, parent_coll_name, comp_to_del_name)

        self.root.navigation.go_back()

    def create_items(self, items: list, header: str, filter_opts: list[str]):
        new_sortable_item_list = SortableItemList(self, self, header, items, len(self.item_list_widgets))
        self.item_list_widgets.append(new_sortable_item_list)
        self.add_sort_buttons(filter_opts, new_sortable_item_list)

    def update_items(self, items: list, index: int):
        sortable_item_list = self.item_list_widgets[index]
        sortable_item_list.update_items(items)

    def refresh_items(self):
        self.root.go_to_homepage()
        self.root.go_to_component(self.component)

    def add_sort_buttons(self, sort_methods: list[str], item_list: SortableItemList):
        for s in sort_methods:
            item_list.add_sort_button(s)

    def collapse_widget(self):
        for child in self.winfo_children():
            child.destroy()
        self.item_list_widgets = []


class SortableItemList(CTkFrame):
    def __init__(self, master,
                 parent: ItemContainer,
                 header: str,
                 items,
                 index: int,
                 **values):
        super().__init__(master, **values)
        self.parent: ItemContainer = parent
        self.header = header
        self.index = index

        self.sort_buttons: list[SortButton] = []
        self.active_sort_button: SortButton = None
        self._children_buttons: list = []

        self.items: list[ITEM] = items
        self.widget_items: list[Item] = []

        self.selected_items: list[Item] = []

        # ===== Widgets ==== #

        self.item_label = CTkLabel(self.parent, text=f"{header} [{len(self.items)}]", font=('Lato', 20), anchor='w')
        self.item_label.pack(fill='x', padx=10, pady=5)

        if not self.parent.homepage:
            self.management_buttons_frame = CTkFrame(self.parent, fg_color='transparent')
            self.management_buttons_frame.pack(fill='x', pady=5)

            self.add_button = CTkButton(self.management_buttons_frame,
                                        text="+ Add Entry",
                                        font=('Lato', 18),
                                        fg_color='green',
                                        width=35,
                                        corner_radius=0,
                                        command=self.open_entry_add_window)
            self.add_button.grid(row=0, column=1, sticky='w', padx=5)

            self.del_button = CTkButton(self.management_buttons_frame,
                                        text="Delete Entry",
                                        font=('Lato', 18),
                                        fg_color='red',
                                        width=35,
                                        corner_radius=0,
                                        state='disabled',
                                        command=self.delete_entry)
            self.del_button.grid(row=0, column=2, sticky='w', padx=5)

        self.sort_buttons_frame = CTkFrame(master=self.parent, height=35, fg_color=BG_GRAY_PRIMARY)
        self.sort_buttons_frame.pack(fill='x', padx=10, pady=10)

        self.item_frame = CTkFrame(master=self.parent, fg_color=BG_GRAY_PRIMARY)
        self.item_frame.pack(fill='x', padx=10, pady=10)

        self.update_items(self.items)
        self.set_add_button_message()

        if self.parent.homepage:
            self.add_sort_button('car')

    def set_add_button_message(self):
        if self.parent.homepage:
            return

        if 'scheduled' in self.header.lower().replace(' ', ''):
            self.add_button.configure(text="+ Add Scheduled Entry")
        else:
            self.add_button.configure(text="+ Add Entry")

    def set_delete_button_message(self):
        selected_entries_count = len(self.selected_items)

        if selected_entries_count > 1:
            self.del_button.configure(text=f"Delete Entries ({selected_entries_count})")
            self.del_button.configure(state='normal')
        elif selected_entries_count > 0:
            self.del_button.configure(text=f"Delete Entry")
            self.del_button.configure(state='normal')
        else:
            self.del_button.configure(text=f"Delete Entry")
            self.del_button.configure(state='disabled')

    def delete_entry(self):
        entries = []
        for item in self.selected_items:
            entries.append(item.item_ref)

        self.parent.root.delete_entries(entries)
        self.refresh_items()

    def sort_items(self, sort_key: str, button_ref, reverse: bool):
        if self.active_sort_button and self.active_sort_button != button_ref:
            self.active_sort_button.unfocus()
        self.active_sort_button = button_ref

        self.parent.parent.update_items(self.index, sort_key, reverse)

    def add_sort_button(self, sort_method: str, **kwargs):
        if not self.is_sort_method_already_used(sort_method):

            if len(self._children_buttons) % 2 != 0:
                self.add_separator()

            new_button = SortButton(master=self.sort_buttons_frame,
                                    parent=self,
                                    sort_method=sort_method,
                                    column=len(self._children_buttons),
                                    **kwargs)
            self.sort_buttons.append(new_button)

            self._children_buttons.append(new_button)

    def add_separator(self):
        separator = CTkLabel(self.sort_buttons_frame, text='|', font=('Lato', 25), text_color='white')
        separator.grid(row=0,
                       column=len(self._children_buttons))
        self._children_buttons.append(separator)

    def is_sort_method_already_used(self, sort_method: str) -> bool:
        items = [button.sort_method for button in self.sort_buttons]
        return sort_method in items

    def update_items(self, items: list):
        self.clear_items()
        self.items = []

        for item in items:
            self.create_item(item)

    def refresh_items(self):
        self.parent.refresh_items()

        try:
            self.item_label.configure(text=f"{self.header} [{len(self.widget_items)}]")
        except Exception:
            pass

    def create_item(self, item_obj, row=-1):
        if item_obj.__class__.__name__ == 'ScheduledLogEntry':
            self.create_scheduled_entry(item_obj, row)
        else:
            self.create_log_entry(item_obj, row)

        self.item_label.configure(text=f"{self.header} [{len(self.widget_items)}]")

    def create_log_entry(self, item_obj, row: int = -1):
        if row == -1:
            row = len(self.items)

        new_item = Item(master=self.item_frame,
                        parent=self,
                        item_ref=item_obj,
                        row=row,
                        homepage=self.parent.homepage)
        self.widget_items.append(new_item)

    def create_scheduled_entry(self, item_obj, row: int = -1):
        if row == -1:
            row = len(self.items)

        new_item = ScheduledLogEntryItem(master=self.item_frame,
                                         parent=self,
                                         item_ref=item_obj,
                                         row=row,
                                         homepage=self.parent.homepage)
        self.widget_items.append(new_item)

    def update_item(self, item, item_ref: ITEM, data_to_update: list[str]):
        item.item_ref = item_ref

        if 'all' in data_to_update:
            item.update_all_info()

        mapping = {'desc': item.update_desc,
                   'date': item.update_date,
                   'component': item.update_component,
                   'category': item.update_category,
                   'mileage': item.update_mileage,
                   'custom_info': item.update_custom_info
                   }

        for data in data_to_update:
            mapping.get(data)()

    def clear_items(self):
        for child in self.item_frame.winfo_children():
            child.destroy()
        self.widget_items = []

    def open_entry_edit_window(self, item_ref: ITEM, item_widget):
        self.parent.root.open_entry_edit_window(item_ref, item_widget)

    def open_entry_add_window(self):
        scheduled = 'scheduled' in self.header.lower().replace(' ', '')
        self.parent.root.open_entry_add_window(self, scheduled)


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
    def __init__(self, master, parent: SortableItemList, item_ref: ITEM, row: int = 0, homepage=False, **kwargs):
        super().__init__(master,
                         height=100,
                         fg_color=BLUE_1,
                         corner_radius=0,
                         **kwargs)
        self.parent = parent
        self.homepage = homepage

        self.id = row
        self.item_ref: ITEM = item_ref

        self.custom_info_labels = []

        # ===== Widget ===== #

        self.pack(expand=True, fill='x', padx=10, pady=5)

        self.is_selected = BooleanVar(value=False)

        self.checkbox = CTkCheckBox(self,
                                    text='',
                                    variable=self.is_selected,
                                    width=10,
                                    onvalue=True,
                                    offvalue=False,
                                    command=self.on_entry_selected)
        self.checkbox.grid(row=0, column=0, padx=5, pady=2)

        self.date_label = CTkLabel(self, text=self._get_date(), font=('Lato', 17), width=100)
        self.date_label.grid(row=0, column=1, padx=5, pady=2)

        self.desc_label = CTkLabel(self,
                                   text=self._get_item_name(),
                                   font=('Lato', 17),
                                   wraplength=500,
                                   width=515,
                                   justify='left',
                                   anchor='w')
        self.desc_label.grid(row=0, column=2, padx=5, pady=2)

        if homepage:
            self.parent_car_label = CTkLabel(self,
                                             text=self.item_ref.component.parent.car.car_info.name,
                                             font=('Lato', 17),
                                             wraplength=115,
                                             width=130,
                                             justify='left',
                                             anchor='w')
            self.parent_car_label.grid(row=0, column=3, padx=5, pady=2)

        self.parent_label = CTkLabel(self,
                                     text=self._get_component_name(),
                                     font=('Lato', 17),
                                     wraplength=135,
                                     width=150,
                                     justify='left',
                                     anchor='w')
        self.parent_label.grid(row=0, column=3+self.homepage, padx=5, pady=2)

        self.category_label = CTkLabel(self, text=self._get_item_category(), font=('Lato', 17), width=100)
        self.category_label.grid(row=0, column=4+self.homepage, padx=5, pady=2)

        self.mileage_label = CTkLabel(self,
                                      text=self._get_mileage(),
                                      font=('Lato', 17),
                                      width=115,
                                      justify='left',
                                      anchor='w')
        self.mileage_label.grid(row=0, column=5+self.homepage, padx=5, pady=2)

        self.create_custom_info()

        self.columnconfigure(8, weight=1)

        # ===== Settings Buttons ===== #

        if self.homepage:
            return

        self.option_buttons_frame = CTkFrame(self, fg_color='transparent')
        self.option_buttons_frame.grid(row=0, column=10+self.homepage, sticky="nse", padx=3, pady=5)

        self.option_buttons_frame.rowconfigure(0, weight=1)

        self.edit_button = CTkButton(self.option_buttons_frame,
                                     text='Edit',
                                     font=('Lato', 17),
                                     width=35,
                                     command=self.open_entry_edit_window)
        self.edit_button.grid(row=0, column=0, sticky="nse", padx=3)

    def on_entry_selected(self, *args):
        if self.is_selected.get():
            self.parent.selected_items.append(self)
        else:
            self.parent.selected_items.remove(self)

        self.parent.set_delete_button_message()

    def create_custom_info(self):
        """Refresh and recreate custom info widget from parent item reference."""

        for w in self.custom_info_labels:
            w.destroy()

        self.custom_info_labels.clear()
        self._destroy_custom_info_placeholder()
        self.create_custom_info_widgets()

    def create_custom_info_widgets(self):
        """Create custom info widgets from item ref's custom info dictionary."""
        for index, item in enumerate(self.item_ref.custom_info.items()):

            if self._is_max_custom_info_display_count_reached():
                try:
                    self.custom_info_clamp_count_label.configure(text=f"+{self._get_clamped_custom_info_count()}")
                except AttributeError:
                    placeholder_index = self._last_custom_info_index + 1
                    self._add_custom_info_placeholder_widget(placeholder_index)

                return
            else:
                new_label = CTkLabel(self,
                                     text=self._format_info(item),
                                     font=('Lato', 17),
                                     wraplength=135,
                                     width=150,
                                     justify='left',
                                     anchor='w')
                new_label.grid(row=0, column=index + 6, padx=5, pady=2)

                self._last_custom_info_index = index + 6

                self.custom_info_labels.append(new_label)

    def _format_info(self, item: tuple[str, ...]) -> str:
        return f"{item[0]}: {item[1]}"

    def _is_max_custom_info_display_count_reached(self):
        if len(self.custom_info_labels) > 2:
            return True
        return False

    def _add_custom_info_placeholder_widget(self, index: int):
        """Create placeholder widget for custom info if the cap has been reached."""
        self.custom_info_clamp_count_label = CTkLabel(self,
                                                      text=f"+{self._get_clamped_custom_info_count()}",
                                                      font=('Lato', 17),
                                                      width=100,
                                                      anchor='w')
        self.custom_info_clamp_count_label.grid(row=0, column=index, padx=5, pady=2)

    def _destroy_custom_info_placeholder(self):
        try:
            self.custom_info_clamp_count_label.destroy()
            del self.custom_info_clamp_count_label
        except AttributeError:
            return

    def _get_clamped_custom_info_count(self) -> int:
        return len(self.item_ref.custom_info.keys())-len(self.custom_info_labels)

    def update_date(self):
        self.date_label.configure(text=self._get_date())

    def update_desc(self):
        self.desc_label.configure(text=self.item_ref.desc)

    def update_component(self):
        self.parent_label.configure(text=self.item_ref.component.name)

    def update_category(self):
        self.category_label.configure(text=self._get_item_category())

    def update_mileage(self):
        self.mileage_label.configure(text=self._get_mileage())

    def update_custom_info(self):
        self.create_custom_info()

    def update_all_info(self):
        self.update_desc()
        self.update_date()
        self.update_component()
        self.update_category()
        self.update_mileage()
        self.update_custom_info()

    def _get_item_name(self) -> str:
        properties = self.item_ref.to_json().get('name', ''), self.item_ref.to_json().get('desc', ''), ''
        return sorted(properties, reverse=True)[0]

    def _get_component_name(self) -> str:
        sep = self.item_ref.component.name.replace('_', ' ')
        return sep.capitalize()

    def _get_item_category(self) -> str:
        cat_str = self.item_ref.category.replace('_', ' ')
        cat_str = cat_str.split(' ')
        cat_str = ' '.join([c.capitalize() for c in cat_str])
        return cat_str

    def _get_date(self):
        return self.item_ref.date

    def _get_mileage(self):
        return f"{self.item_ref.mileage} km"

    def open_entry_edit_window(self):
        self.parent.open_entry_edit_window(self.item_ref, self)


class ScheduledLogEntryItem(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.homepage:
            return

        self.complete_button = CTkButton(self.option_buttons_frame,
                                         text='➕',
                                         font=('Lato', 17),
                                         width=35,
                                         command=self.mark_entry_as_complete)
        self.complete_button.grid(row=0, column=1, sticky="nse", padx=3)

        self._set_time_remaining_text_color()

    def _get_item_name(self) -> str:
        properties = self.item_ref.to_json().get('name', ''), self.item_ref.to_json().get('desc', ''), ''
        return sorted(properties, reverse=True)[0]

    def _get_date(self) -> str:
        if self.item_ref.get_schedule_rule() == 'date':
            return f"{self.item_ref.date}\n" \
                   f"({self.item_ref.time_remaining_to_str()})"

        return self.item_ref.date

    def _set_time_remaining_text_color(self):
        if self.item_ref.get_time_remaining() < 0:
            match self.item_ref.get_schedule_rule():
                case 'date': self.date_label.configure(text_color='red')
                case 'mileage': self.mileage_label.configure(text_color='red')
        else:
            match self.item_ref.get_schedule_rule():
                case 'date': self.date_label.configure(text_color='white')
                case 'mileage': self.mileage_label.configure(text_color='white')

    def _get_mileage(self):
        if self.item_ref.get_schedule_rule() == 'mileage':
            return f"{self.item_ref.mileage} km\n" \
                   f"(in {abs(self.item_ref.get_time_remaining())} km)"

        return f"{self.item_ref.mileage} km"

    def mark_entry_as_complete(self):
        entry = self.parent.parent.app_session.set_scheduled_entry_as_done(self.parent.parent.parent_car, self.item_ref)
        self.parent.update_item(self, entry, ['date', 'mileage'])

        new_entry = self.item_ref.component.latest_entry
        self.parent.parent.item_list_widgets[1].create_log_entry(new_entry)
        self.parent.refresh_items()
