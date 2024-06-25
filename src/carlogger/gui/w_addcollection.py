from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkScrollableFrame

from tkinter import StringVar


class AddCollectionPopup:
    def __init__(self, master, root, parent_car):
        self.master = master
        self.root = root
        self.parent_car = parent_car

        self.required_fields: list[str] = ['name', 'custom_info']

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

        self.label = CTkLabel(self.top_frame, text="Add Collection", font=('Lato', 30))
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

        # ===== Add Collection Button ===== #

        self.addb_frame = CTkFrame(self.add_main_frame, fg_color='transparent')
        self.addb_frame.grid(row=1, column=0, sticky='w', pady=10)

        self.add_button = CTkButton(self.addb_frame,
                                    text="Create Collection",
                                    font=('Lato', 20),
                                    fg_color='green',
                                    corner_radius=10,
                                    command=self.add_collection,
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

        # ===== Custom Info ===== #

        self.custom_frame = CTkScrollableFrame(self.add_mid_frame, fg_color='transparent', width=550, height=400)
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

        updated_data['custom_info'] = self.property_container.get_properties()

        return updated_data

    def _has_all_necessary_fields(self, values: dict) -> bool:
        keys = list(values.keys())
        return sorted(keys) == sorted(self.required_fields)

    def add_collection(self):
        coll_data = self.collect_changes()

        if not self._has_all_necessary_fields(coll_data):
            self.add_label.configure(text="There is missing information.")
            return

        self.root.app_session.add_new_collection(self.parent_car.car_info.name, coll_data['name'])

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
        self.root.go_to_car(self.parent_car)

    def close_menu(self, *args):
        self.overlay_frame.destroy()
        self.popup_frame.destroy()
        del self


class PropertyContainer(CTkFrame):
    def __init__(self, master, root: CTk, parent: AddCollectionPopup, **values):
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
        val = self.property_value_car.get()
        if val.isdigit():
            if val.find(".") != -1 or val.find(",") != -1:
                return float(val)
            else:
                return int(val)
        else:
            return val
