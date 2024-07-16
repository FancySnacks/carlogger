from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkScrollableFrame, CTkOptionMenu

from tkinter import StringVar

from carlogger.util import dict_diff


class EditComponentPopup:
    def __init__(self, master, root, parent_car, collection_ref, component_ref, itembox_ref):
        self.master = master
        self.root = root
        self.itembox_ref = itembox_ref

        self.parent_car = parent_car
        self.collection_ref = collection_ref
        self.component_ref = component_ref
        self.og_item_values = self.component_ref.to_json()

        # ===== Overlay Frame ===== #

        self.overlay_frame = CTkFrame(self.master, bg_color='transparent')
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ===== Main Popup Frame ===== #

        self.popup_frame = CTkFrame(self.master, width=1200, height=600, corner_radius=10, bg_color='transparent')
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

        self.label = CTkLabel(self.top_frame, text="Edit Component", font=('Lato', 30))
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

        self.saveb_frame = CTkFrame(self.add_main_frame, fg_color='transparent')
        self.saveb_frame.grid(row=1, column=0, sticky='w', pady=10)

        self.saveb_button = CTkButton(self.saveb_frame,
                                      text="Update Component",
                                      font=('Lato', 20),
                                      fg_color='green',
                                      corner_radius=10,
                                      command=self.update_component,
                                      state='disabled')
        self.saveb_button.grid(row=0, column=0, sticky='w', padx=15, pady=5)

        self.saveb_label = CTkLabel(self.saveb_frame, text="", font=('Lato', 16))
        self.saveb_label.grid(row=0, column=1, sticky='w')

        # ===== Name ===== #

        self.name_var = StringVar(value=self.og_item_values['name'])
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

        # ===== Parents ===== #

        self.parent_frame = CTkFrame(self.add_left_frame, fg_color='transparent')
        self.parent_frame.grid(row=2, column=0, sticky='w', pady=10, columnspan=3, padx=10)

        ## Car
        self.car_frame = CTkFrame(self.parent_frame, fg_color='transparent')
        self.car_frame.grid(row=0, column=0, sticky='w', pady=10)

        self.car_label = CTkLabel(self.car_frame, text="Car", font=('Lato', 20))
        self.car_label.grid(row=0, column=0, sticky='w')

        self.car_menu = CTkOptionMenu(self.car_frame,
                                      values=self.get_car_names(),
                                      command=self.on_car_changed)
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
                                             command=self.on_collection_changed)
        self.collection_menu.grid(row=1, column=0, sticky='w')
        self.collection_menu.set(self.collection_ref.name)

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
                                                    item_ref=self.component_ref,
                                                    width=250,
                                                    fg_color='transparent')
        self.property_container.grid(row=1, column=0, columnspan=5, sticky='w')

        self.property_container.create_properties()

    def add_new_property(self):
        self.property_container.add_property()
        self.track_changes()

    def get_collection_names(self) -> list[str]:
        return [coll.name for coll in self.parent_car.collections]

    def get_car_names(self) -> list[str]:
        return [car.car_info.name for car in self.root.cars]

    def on_car_changed(self, choice):
        car_choice = choice
        self.new_car = self.root.app_session.get_car_by_name(car_choice)
        collection_names = [coll.name for coll in self.parent_car.collections]
        self.collection_menu.configure(values=collection_names)
        self.collection_menu.set(collection_names[0])
        self.track_changes()

    def on_collection_changed(self, choice):
        coll_choice = choice
        self.new_coll = self.parent_car.get_collection_by_name(coll_choice)
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
        updated_data = dict_diff(updated_data, self.og_item_values)

        return updated_data

    def update_component(self):
        comp_data = self.collect_changes()

        self._reset_button()
        try:
            if self.new_coll != self.component_ref.parent:
                comp_data['parent'] = self.new_coll
        except Exception as e:
            pass
        self.root.app_session.update_component_or_collection(self.parent_car, self.component_ref, comp_data)

    def track_changes(self, *args):
        changed_data = self.collect_changes()

        if changed_data == self.og_item_values:
            self._reset_button()
        else:
            self._enable_button()

        try:
            if self.new_coll != self.component_ref.parent:
                self._enable_button()
            else:
                self._reset_button()
        except Exception as e:
            pass

    def _reset_button(self, *args):
        self.saveb_button.configure(state='disabled')
        self.saveb_label.configure(text='')

    def _enable_button(self):
        self.saveb_button.configure(state='normal')
        self.saveb_label.configure(text="There are unsaved changes.")

    def close_menu(self, *args):
        self.overlay_frame.destroy()
        self.popup_frame.destroy()
        self.itembox_ref.refresh_info()
        del self


class PropertyContainer(CTkFrame):
    def __init__(self, master, root: CTk, parent: EditComponentPopup, item_ref, **values):
        super().__init__(master, **values)
        self.master = master
        self.root = root
        self.parent = parent
        self.item_ref = item_ref

        self.properties: dict[str, ...] = item_ref.custom_info.copy()
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

    def delete_property(self, key: str):
        self.properties.pop(key)

        for widget in self.property_widgets:
            if widget.property_name.get() == key:
                widget.property_frame.destroy()
                self.property_widgets.remove(widget)
                break

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
        self.master.delete_property(self.property_name.get())

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
