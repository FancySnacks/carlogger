from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, \
    CTkTextbox, CTkOptionMenu, CTkScrollableFrame

from tkinter import END, StringVar

from carlogger.gui.w_itemlist import SortableItemList
from carlogger.items.entry_category import EntryCategory
from carlogger.util import is_date
from carlogger.const import TODAY


class AddEntryPopup:
    def __init__(self, master, root, item_list: SortableItemList, parent_component, scheduled_entry: bool = False):
        self.master = master
        self.root = root
        self.item_list = item_list
        
        self.is_scheduled_entry = scheduled_entry
        self.required_fields: list[str] = ['category', 'component', 'date', 'desc', 'mileage', 'custom_info', 'tags']

        if self.is_scheduled_entry:
            self.required_fields.extend(['frequency'])
            self.required_fields.extend(['rule'])
            self.required_fields.extend(['repeating'])

        self.cars = self.root.cars
        self.car_names = [car.car_info.name for car in self.cars]
        self.current_component = parent_component
        self.current_collection = self.current_component.parent

        # ===== Widget ===== #

        self.main_frame = CTkFrame(self.master)
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.top_frame = CTkFrame(self.main_frame, fg_color='transparent')
        self.top_frame.pack(anchor='w')

        self.back_button = CTkButton(self.top_frame,
                                     text="<",
                                     font=('Lato', 50),
                                     width=5,
                                     corner_radius=0,
                                     anchor='center',
                                     fg_color='transparent',
                                     command=self.close_menu)
        self.back_button.grid(row=0, column=0, pady=5, padx=10, sticky='w')

        self.label = CTkLabel(self.top_frame, text="Add" 
                                                   f"{' Scheduled' if self.is_scheduled_entry else ''}"
                                                   " Entry",
                              font=('Lato', 30))
        self.label.grid(row=0, column=1, pady=5, padx=10, sticky='w')

        self.separator = CTkLabel(self.main_frame, text='', bg_color='gray', height=1, font=('Arial', 2))
        self.separator.pack(fill='x', padx=10)
        
        # ===== Add Section Frames ===== #

        self.add_main_frame = CTkScrollableFrame(self.main_frame, fg_color='transparent', height=1900)
        self.add_main_frame.pack(anchor='center', fill='both', pady=10, padx=15)

        self.add_left_frame = CTkFrame(self.add_main_frame, fg_color='#403f3f')
        self.add_left_frame.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add_mid_frame = CTkFrame(self.add_main_frame, fg_color='#403f3f')
        self.add_mid_frame.grid(row=0, column=1, sticky='nsew', pady=10, padx=10)

        # ===== Add Entry Button ===== #

        self.addb_frame = CTkFrame(self.add_main_frame, fg_color='transparent')
        self.addb_frame.grid(row=1, column=0, sticky='w')

        self.add_button = CTkButton(self.addb_frame,
                                    text="Create Entry",
                                    font=('Lato', 20),
                                    fg_color='green',
                                    corner_radius=10,
                                    command=self.add_entry,
                                    state='disabled')
        self.add_button.grid(row=0, column=0, sticky='w', padx=15, pady=5)

        self.add_label = CTkLabel(self.addb_frame, text="", font=('Lato', 16))
        self.add_label.grid(row=0, column=1, sticky='w')

        # ===== Date ===== #

        self.date_var = StringVar(value=TODAY)

        self.date_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.date_frame.grid(row=0, column=0, sticky='w', pady=10, padx=10)

        self.date_label = CTkLabel(self.date_frame, text="Date", font=('Lato', 20))
        self.date_label.grid(row=0, column=0, sticky='w')

        self.date_entry = CTkEntry(self.date_frame,
                                   font=('Lato', 20),
                                   placeholder_text='Enter date (DD-MM-YYYY)',
                                   textvariable=self.date_var)
        self.date_entry.grid(row=1, column=0, sticky='w')

        self.date_var.trace_add('write', self.track_changes)

        self.date_hint_label = CTkLabel(self.date_frame, text="format: DD-MM-YYYY", font=('Lato', 12))
        self.date_hint_label.grid(row=2, column=0, sticky='w', pady=3)

        # ===== Desc ===== #

        self.desc_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.desc_frame.grid(row=1, column=0, sticky='w', pady=10, padx=10)

        self.desc_label = CTkLabel(self.desc_frame, text="Description", font=('Lato', 20))
        self.desc_label.grid(row=0, column=0, sticky='w')

        self.desc_entry = CTkTextbox(self.desc_frame, font=('Lato', 20), width=580, height=100)
        self.desc_entry.grid(row=1, column=0, sticky='w')

        self.desc_entry.bind('<Key>', self.track_changes)

        # ===== Parents ===== #

        self.parent_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.parent_frame.grid(row=2, column=0, sticky='w', pady=10, columnspan=3, padx=10)

        # Car

        self.car_frame = CTkFrame(self.parent_frame, fg_color='transparent')
        self.car_frame.grid(row=0, column=0, sticky='w', pady=10)

        self.car_label = CTkLabel(self.car_frame, text="Car", font=('Lato', 20))
        self.car_label.grid(row=0, column=0, sticky='w')

        self.car_menu = CTkOptionMenu(self.car_frame,
                                      values=self.car_names,
                                      command=self.on_car_selection_change)
        self.car_menu.set(self.root.selected_car.car_info.name)
        self.car_menu.grid(row=1, column=0, sticky='w')

        separator = CTkLabel(self.car_frame, text="->", font=('Lato', 20))
        separator.grid(row=1, column=1, sticky='w', padx=10)

        # Collection

        self.collection_frame = CTkFrame(self.parent_frame, fg_color='transparent')
        self.collection_frame.grid(row=0, column=1, sticky='w', pady=10)

        self.collection_label = CTkLabel(self.collection_frame, text="Collection", font=('Lato', 20))
        self.collection_label.grid(row=0, column=0, sticky='w')

        self.collection_menu = CTkOptionMenu(self.collection_frame,
                                             values=self.get_collection_names(),
                                             command=self.on_collection_selection_change)
        self.collection_menu.grid(row=1, column=0, sticky='w')

        self.collection_menu.set(self.current_collection.name)

        separator = CTkLabel(self.collection_frame, text="->", font=('Lato', 20))
        separator.grid(row=1, column=1, sticky='w', padx=10)

        # Component

        self.component_frame = CTkFrame(self.parent_frame, fg_color='transparent')
        self.component_frame.grid(row=0, column=2, sticky='w', pady=10)

        self.component_label = CTkLabel(self.component_frame, text="Component", font=('Lato', 20))
        self.component_label.grid(row=0, column=0, sticky='w')

        self.component_menu = CTkOptionMenu(self.component_frame,
                                            values=self.get_component_names(),
                                            command=self.on_component_selection_change)
        self.component_menu.grid(row=1, column=0, sticky='w')

        self.component_menu.set(self.current_component.name)

        # ===== Category ===== #

        self.category_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.category_frame.grid(row=5, column=0, sticky='w', pady=10, padx=10)

        self.category_label = CTkLabel(self.category_frame, text="Category", font=('Lato', 20))
        self.category_label.grid(row=0, column=0, sticky='w')

        self.category_menu = CTkOptionMenu(self.category_frame,
                                           values=[e for e in EntryCategory],
                                           command=self.on_category_selection_change)
        self.category_menu.grid(row=1, column=0, sticky='w')

        # ===== Mileage ===== #

        self.mileage_var = StringVar(value=self.current_component.current_mileage)

        self.mileage_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.mileage_frame.grid(row=6, column=0, sticky='w', pady=10, padx=10)

        self.mileage_label = CTkLabel(self.mileage_frame, text="Mileage", font=('Lato', 20))
        self.mileage_label.grid(row=0, column=0, sticky='w')

        self.mileage_entry = CTkEntry(self.mileage_frame,
                                      font=('Lato', 20),
                                      placeholder_text='Enter mileage (km)',
                                      textvariable=self.mileage_var)
        self.mileage_entry.grid(row=1, column=0, sticky='w')

        self.mileage_unit_label = CTkLabel(self.mileage_frame, text="km", font=('Lato', 20))
        self.mileage_unit_label.grid(row=1, column=1, sticky='w', padx=10)

        self.mileage_var.trace_add('write', self.track_changes)

        # ===== Custom Info ===== #

        self.custom_frame = CTkScrollableFrame(self.add_mid_frame, fg_color='transparent', width=550, height=800)
        self.custom_frame.grid(row=0, column=0, sticky='w', pady=10, padx=10)

        self.custom_label = CTkLabel(self.custom_frame, text="Custom Properties", font=('Lato', 20))
        self.custom_label.grid(row=0, column=0, sticky='w')

        self.add_property_button = CTkButton(self.custom_frame,
                                             text="+",
                                             font=('Lato', 20),
                                             fg_color='green',
                                             width=35,
                                             corner_radius=0,
                                             command=self.add_new_property)
        self.add_property_button.grid(row=0, column=1, sticky='w', padx=15, pady=5)

        self.property_container = PropertyContainer(self.custom_frame,
                                                    self.root,
                                                    self,
                                                    width=250,
                                                    fg_color='transparent')
        self.property_container.grid(row=1, column=0, columnspan=5, sticky='w')

        self.property_container.create_properties()

        if self.is_scheduled_entry:

            # ===== ScheduledLogEntry Options ===== #

            self.edit_right_frame = CTkFrame(self.add_main_frame, fg_color='#403f3f', width=300)
            self.edit_right_frame.grid(row=0, column=2, sticky='nsew', pady=10, padx=10)

            # ===== Frequency ===== #

            self.frequency_var = StringVar(value="7")

            self.frequency_frame = CTkFrame(self.edit_right_frame, fg_color='transparent', width=300)
            self.frequency_frame.grid(row=0, column=0, sticky='w', pady=10, padx=10)

            self.frequency_label = CTkLabel(self.frequency_frame, text="Frequency", font=('Lato', 20))
            self.frequency_label.grid(row=0, column=0, sticky='w')

            self.frequency_entry = CTkEntry(self.frequency_frame,
                                            font=('Lato', 20),
                                            placeholder_text='Frequency',
                                            textvariable=self.frequency_var)
            self.frequency_entry.grid(row=1, column=0, sticky='w')

            self.frequency_unit_label = CTkLabel(self.frequency_frame,
                                                 text='days / km',
                                                 font=('Lato', 20))
            self.frequency_unit_label.grid(row=1, column=1, sticky='w')

            self.frequency_hint_label = CTkLabel(self.frequency_frame,
                                                 text="Leave empty for one-time entry",
                                                 font=('Lato', 12))
            self.frequency_hint_label.grid(row=2, column=0, sticky='w', pady=3)

            self.frequency_var.trace_add('write', self.track_changes)

            # ===== Rule ===== #

            self.rule_frame = CTkFrame(self.edit_right_frame, fg_color='transparent', width=550)
            self.rule_frame.grid(row=1, column=0, sticky='w', pady=10, padx=10)

            self.rule_label = CTkLabel(self.rule_frame, text="Rule", font=('Lato', 20))
            self.rule_label.grid(row=0, column=0, sticky='w')

            self.rule_menu = CTkOptionMenu(self.rule_frame,
                                           values=['date', 'mileage'],
                                           command=self.on_rule_selection_change)
            self.rule_menu.grid(row=1, column=0, sticky='w')

    def on_category_selection_change(self, selected_option):
        self.track_changes(selected_option)

    def on_rule_selection_change(self, selected_option):
        self.track_changes(selected_option)

    def on_car_selection_change(self, selected_option):
        colls = [collection.name for collection in self.root.selected_car.collections]
        self.collection_menu.configure(values=colls)
        self.component_menu.set(colls[0])

        self.track_changes(selected_option)

    def on_collection_selection_change(self, selected_option):
        self.current_collection = self.root.selected_car.get_collection_by_name(selected_option)
        comps = [component.name for component in self.current_collection.components]
        self.component_menu.configure(values=comps)
        self.component_menu.set(comps[0])

        self.track_changes(selected_option)

    def on_component_selection_change(self, selected_option):
        self.track_changes(selected_option)

    def get_collection_names(self) -> list[str]:
        return [coll.name for coll in self.root.selected_car.collections]

    def get_component_names(self) -> list[str]:
        return [comp.name for comp in self.current_collection.components]

    def add_new_property(self):
        self.property_container.add_property()
        self.track_changes()

    def collect_changes(self):
        updated_data: dict = dict()

        date = self.date_entry.get()
        if is_date(date):
            updated_data['date'] = date
            self.date_entry.configure(border_color='')
        else:
            self.date_entry.configure(border_color='red')

        desc = self.desc_entry.get(1.0, END).strip()
        if desc:
            updated_data['desc'] = desc

        comp = self.current_collection.get_component_by_name(self.component_menu.get())
        if comp:
            updated_data['component'] = comp

        updated_data['category'] = self.category_menu.get()

        mileage = self.mileage_var.get()
        if not mileage.isdigit():
            mileage = 0
        updated_data['mileage'] = int(mileage)

        updated_data['custom_info'] = self.property_container.get_properties()

        if self.is_scheduled_entry:
            frequency = self.frequency_var.get()

            if frequency != "" and int(frequency) > 0:
                updated_data['frequency'] = int(frequency)
                updated_data['repeating'] = True
            else:
                updated_data['frequency'] = 0
                updated_data['repeating'] = False

            updated_data['rule'] = self.rule_menu.get().lower()

        updated_data['tags'] = []

        return updated_data

    def _has_all_necessary_fields(self, values: dict) -> bool:
        keys = list(values.keys())
        return sorted(keys) == sorted(self.required_fields)

    def add_entry(self):
        entry_data = self.collect_changes()

        if not self._has_all_necessary_fields(entry_data):
            self.add_label.configure(text="There is missing information.")
            return

        if self.is_scheduled_entry:
            self.root.app_session.add_new_scheduled_entry(self.root.selected_car.car_info.name,
                                                          self.current_collection.name,
                                                          self.current_component.name,
                                                          entry_data)
        else:
            self.root.app_session.add_new_entry(self.root.selected_car.car_info.name,
                                                self.current_collection.name,
                                                self.current_component.name,
                                                entry_data)

        self._post_entry_add()

    def track_changes(self, *args):
        changed_data = self.collect_changes()

        if changed_data == {}:
            self._reset_button()
        else:
            self._enable_button()

    def _reset_button(self, *args):
        self.add_button.configure(state='disabled')
        self.add_label.configure(text='')

    def _enable_button(self):
        self.add_button.configure(state='normal')
        self.add_label.configure(text='')

    def _post_entry_add(self):
        self.close_menu()
        self.item_list.refresh_items()

    def close_menu(self, *args):
        self.main_frame.destroy()
        del self


class PropertyContainer(CTkFrame):
    def __init__(self, master, root: CTk, parent: AddEntryPopup, **values):
        super().__init__(master, **values)
        self.master = master
        self.root = root
        self.parent = parent

        self.properties: dict[str, ...] = dict()
        self.property_widgets: list[PropertyItem] = []

    def get_properties(self) -> dict:
        d = {}
        for pw in self.property_widgets:
            d[pw.property_name.get()] = pw.get_val()

        return d

    def add_property(self, name: str = 'New Property', value='Enter value'):
        new_item = PropertyItem(self, self.root, name, value, len(self.property_widgets))
        self.property_widgets.append(new_item)
        self.properties[name] = value

    def delete_property(self, index: int, key: str):
        self.properties.pop(key)
        item = self.property_widgets.pop(index)
        item.property_frame.destroy()
        self.track_changes()

    def create_properties(self):
        for p in self.properties.items():
            self.add_property(p[0], p[1])

    def track_changes(self):
        self.parent.track_changes()


class PropertyItem:
    def __init__(self, master, root: CTk, property_name: str, property_value, index: int):
        self.master = master
        self.root = root

        self.index: int = index
        
        self.og_property_name = property_name
        self.og_property_value = property_value

        self.property_name = StringVar(value=property_name)
        self.property_value = StringVar(value=property_value)

        # ===== Widget ===== #

        self.property_frame = CTkFrame(self.master, fg_color='gray', width=500)
        self.property_frame.pack(fill='x', anchor='w', padx=2, pady=2)

        self.property_name_entry = CTkEntry(self.property_frame, 
                                            font=('Lato', 17), 
                                            width=200, 
                                            textvariable=self.property_name)
        self.property_name_entry.grid(row=0, column=0, sticky='w', padx=3, pady=2)

        self.separator = CTkLabel(self.property_frame,
                                  text='',
                                  bg_color='lightgray',
                                  height=20,
                                  width=3,
                                  font=('Arial', 2))
        self.separator.grid(row=0, column=1, sticky='w', padx=10)

        self.property_value_entry = CTkEntry(self.property_frame, 
                                             font=('Lato', 17), 
                                             width=280,
                                             textvariable=self.property_value)
        self.property_value_entry.grid(row=0, column=2, sticky='w', padx=3, pady=2)
        
        self.property_name.trace_add('write', self.on_property_update)
        self.property_value.trace_add('write', self.on_property_update)

        self.delete_button = CTkButton(self.property_frame,
                                       text="x",
                                       width=5,
                                       font=('Lato', 20),
                                       text_color='red',
                                       fg_color='gray',
                                       command=self.delete_property)
        self.delete_button.grid(row=0, column=3, sticky='w', padx=3, pady=5)

    def delete_property(self):
        self.master.delete_property(self.index, self.property_name.get())

    def on_property_update(self, *args):
        conditions = any((self.property_name.get() != self.og_property_name, 
                          self.property_value.get() != self.og_property_value))
        
        if conditions:
            self.master.track_changes()

    def get_val(self):
        val = self.property_value_entry.get()
        if val.isdigit():
            if val.find(".") != -1 or val.find(",") != -1:
                return float(val)
            else:
                return int(val)
        else:
            return val
