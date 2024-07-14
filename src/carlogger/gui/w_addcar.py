from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkScrollableFrame

from tkinter import StringVar

from carlogger.const import TODAY
from carlogger.util import date_string_to_date


class AddCarPopup:
    def __init__(self, master, root):
        self.master = master
        self.root = root

        self.required_fields: list[str] = ['name', 'manufacturer', 'model', 'year', 'mileage', 'custom_info']

        # ===== Overlay Frame ===== #
        self.overlay_frame = CTkFrame(self.master, bg_color='transparent')
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ===== Main Popup Frame ===== #
        self.popup_frame = CTkFrame(self.master, width=965, height=600, corner_radius=10, bg_color='transparent')
        self.popup_frame.place(relx=0.5, rely=0.5, anchor='center')

        # ===== Widget ===== #
        self.main_frame = CTkFrame(self.popup_frame)
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

        self.label = CTkLabel(self.top_frame, text="Add Car", font=('Lato', 30))
        self.label.grid(row=0, column=1, pady=5, padx=10, sticky='w')

        self.separator = CTkLabel(self.main_frame, text='', bg_color='gray', height=1, font=('Arial', 2))
        self.separator.pack(fill='x', padx=10)

        # ===== Add Section Frames ===== #
        self.add_main_frame = CTkFrame(self.main_frame, fg_color='#403f3f')
        self.add_main_frame.pack(anchor='center', fill='both', pady=10, padx=15)

        self.add_left_frame = CTkFrame(self.add_main_frame, fg_color='#403f3f')
        self.add_left_frame.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add_mid_frame = CTkFrame(self.add_main_frame, fg_color='#403f3f')
        self.add_mid_frame.grid(row=0, column=1, sticky='nsew', pady=10, padx=10)

        # ===== Add Car Button ===== #
        self.addb_frame = CTkFrame(self.add_main_frame, fg_color='transparent')
        self.addb_frame.grid(row=1, column=0, sticky='w', pady=10)

        self.add_button = CTkButton(self.addb_frame,
                                    text="Create Car",
                                    font=('Lato', 20),
                                    fg_color='green',
                                    corner_radius=10,
                                    command=self.add_car,
                                    state='disabled')
        self.add_button.grid(row=0, column=0, sticky='w', padx=15, pady=5)

        self.add_label = CTkLabel(self.addb_frame, text="", font=('Lato', 16))
        self.add_label.grid(row=0, column=1, sticky='w')

        # ===== Name ===== #
        self.name_var = StringVar()
        self.name_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.name_frame.grid(row=0, column=0, sticky='w', pady=10, padx=10)

        self.name_label = CTkLabel(self.name_frame, text="Name", font=('Lato', 20))
        self.name_label.grid(row=0, column=0, sticky='w')

        self.name_entry = CTkEntry(self.name_frame,
                                   font=('Lato', 20),
                                   textvariable=self.name_var,
                                   width=250)
        self.name_entry.grid(row=1, column=0, sticky='w')

        self.name_var.trace_add('write', self.track_changes)

        # ===== Manufacturer ===== #
        self.manufacturer_var = StringVar()
        self.manufacturer_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.manufacturer_frame.grid(row=1, column=0, sticky='w', pady=10, padx=10)

        self.manufacturer_label = CTkLabel(self.manufacturer_frame, text="Manufacturer", font=('Lato', 20))
        self.manufacturer_label.grid(row=0, column=0, sticky='w')

        self.manufacturer_entry = CTkEntry(self.manufacturer_frame, font=('Lato', 20),
                                           textvariable=self.manufacturer_var,
                                           width=250)
        self.manufacturer_entry.grid(row=1, column=0, sticky='w')

        self.manufacturer_var.trace_add('write', self.track_changes)

        # ===== Model ===== #
        self.model_var = StringVar()
        self.model_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.model_frame.grid(row=2, column=0, sticky='w', pady=10, padx=10)

        self.model_label = CTkLabel(self.model_frame, text="Model", font=('Lato', 20))
        self.model_label.grid(row=0, column=0, sticky='w')

        self.model_entry = CTkEntry(self.model_frame,
                                    font=('Lato', 20),
                                    textvariable=self.model_var,
                                    width=250)
        self.model_entry.grid(row=1, column=0, sticky='w')

        self.model_var.trace_add('write', self.track_changes)

        # ===== Year ===== #
        self.year_var = StringVar(value=str(date_string_to_date(TODAY).year))
        self.year_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.year_frame.grid(row=3, column=0, sticky='w', pady=10, padx=10)

        self.year_label = CTkLabel(self.year_frame, text="Year", font=('Lato', 20))
        self.year_label.grid(row=0, column=0, sticky='w')

        self.year_entry = CTkEntry(self.year_frame,
                                   font=('Lato', 20),
                                   textvariable=self.year_var)
        self.year_entry.grid(row=1, column=0, sticky='w')

        self.year_var.trace_add('write', self.track_changes)

        # ===== Mileage ===== #
        self.mileage_var = StringVar(value="0")
        self.mileage_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.mileage_frame.grid(row=4, column=0, sticky='w', pady=10, padx=10)

        self.mileage_label = CTkLabel(self.mileage_frame, text="Mileage", font=('Lato', 20))
        self.mileage_label.grid(row=0, column=0, sticky='w')

        self.mileage_entry = CTkEntry(self.mileage_frame,
                                      font=('Lato', 20),
                                      placeholder_text='Enter mileage (km)',
                                      textvariable=self.mileage_var,
                                      width=250)
        self.mileage_entry.grid(row=1, column=0, sticky='w')

        self.mileage_unit_label = CTkLabel(self.mileage_frame, text="km", font=('Lato', 20))
        self.mileage_unit_label.grid(row=1, column=1, sticky='w', padx=10)

        self.mileage_var.trace_add('write', self.track_changes)

        # ===== Custom Info ===== #
        self.custom_frame = CTkScrollableFrame(self.add_mid_frame, fg_color='transparent', width=625, height=400)
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

    def add_new_property(self):
        self.property_container.add_property()
        self.track_changes()

    def collect_changes(self):
        updated_data: dict = dict()

        name = self.name_entry.get()
        if name:
            updated_data['name'] = name
            self.name_entry.configure(border_color='')
        else:
            self.name_entry.configure(border_color='red')

        manufacturer = self.manufacturer_entry.get()
        if manufacturer:
            updated_data['manufacturer'] = manufacturer
            self.manufacturer_entry.configure(border_color='')
        else:
            self.manufacturer_entry.configure(border_color='red')

        model = self.model_entry.get()
        if model:
            updated_data['model'] = model
            self.model_entry.configure(border_color='')
        else:
            self.model_entry.configure(border_color='red')

        year = self.year_entry.get()
        if model:
            updated_data['year'] = year
            self.year_entry.configure(border_color='')
        else:
            self.year_entry.configure(border_color='red')

        mileage = self.mileage_var.get()
        if not mileage.isdigit():
            mileage = 0
        updated_data['mileage'] = int(mileage)

        updated_data['custom_info'] = self.property_container.get_properties()

        return updated_data

    def _has_all_necessary_fields(self, values: dict) -> bool:
        keys = list(values.keys())
        return sorted(keys) == sorted(self.required_fields)

    def add_car(self):
        car_data = self.collect_changes()

        if not self._has_all_necessary_fields(car_data):
            self.add_label.configure(text="There is missing information.")
            return

        self.root.app_session.add_new_car(car_data)

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
        self.root.go_to_homepage()

    def close_menu(self, *args):
        self.overlay_frame.destroy()
        self.popup_frame.destroy()
        del self


class PropertyContainer(CTkFrame):
    def __init__(self, master, root: CTk, parent: AddCarPopup, **values):
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

    def move_property(self, offset: int, property_item):
        new_index = min(max(self.property_widgets.index(property_item) + offset, 0), len(self.property_widgets)-1)

        items = list(self.properties.items())

        # Delete the original item so it can be reinserted at other index
        i_to_del = -1
        for i in range(0, len(items)):
            if items[i][0] == property_item.property_name.get():
                i_to_del = i
        if i_to_del > -1:
            items.pop(i_to_del)

        items.insert(new_index, (property_item.property_name.get(), property_item.property_value.get()))

        self.properties = {k: v for k, v in items}

        for widget in self.property_widgets:
            widget.property_frame.destroy()
            del widget

        self.property_widgets.clear()
        self.create_properties()


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

        self.property_name_car = CTkEntry(self.property_frame,
                                          font=('Lato', 17),
                                          width=200,
                                          textvariable=self.property_name)
        self.property_name_car.grid(row=0, column=0, sticky='w', padx=3, pady=2)

        self.separator = CTkLabel(self.property_frame,
                                  text='',
                                  bg_color='lightgray',
                                  height=20,
                                  width=3,
                                  font=('Arial', 2))
        self.separator.grid(row=0, column=1, sticky='w', padx=10)

        self.property_value_car = CTkEntry(self.property_frame,
                                           font=('Lato', 17),
                                           width=280,
                                           textvariable=self.property_value)
        self.property_value_car.grid(row=0, column=2, sticky='w', padx=3, pady=2)

        self.property_name.trace_add('write', self.on_property_update)
        self.property_value.trace_add('write', self.on_property_update)

        self.move_up_button = CTkButton(self.property_frame,
                                        text="^",
                                        font=('Lato', 20),
                                        width=35,
                                        corner_radius=0,
                                        command=self.move_property_up)
        self.move_up_button.grid(row=0, column=3, sticky='w', padx=3, pady=5)

        self.move_down_button = CTkButton(self.property_frame,
                                          text="v",
                                          font=('Lato', 20),
                                          width=35,
                                          corner_radius=0,
                                          command=self.move_property_down)
        self.move_down_button.grid(row=0, column=4, sticky='w', padx=3, pady=5)

        self.delete_button = CTkButton(self.property_frame,
                                       text="x",
                                       width=5,
                                       font=('Lato', 20),
                                       text_color='red',
                                       fg_color='gray',
                                       command=self.delete_property)
        self.delete_button.grid(row=0, column=5, sticky='w', padx=3, pady=5)

    def delete_property(self):
        self.master.delete_property(self.index, self.property_name.get())

    def move_property_up(self):
        self.master.move_property(-1, self)

    def move_property_down(self):
        self.master.move_property(1, self)

    def on_property_update(self, *args):
        conditions = any((self.property_name.get() != self.og_property_name,
                          self.property_value.get() != self.og_property_value))

        if conditions:
            self.master.track_changes()

    def get_val(self):
        val = self.property_value_car.get()
        if val.isdigit():
            if val.find(".") != -1 or val.find(",") != -1:
                return float(val)
            else:
                return int(val)
        else:
            return val
