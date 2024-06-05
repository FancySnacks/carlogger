from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkTextbox, CTkOptionMenu, CTkScrollableFrame

from tkinter import END

from carlogger.items.entry_category import EntryCategory


class EditEntryPopup:
    def __init__(self, master, root: CTk, item_ref):
        self.master = master
        self.root = root
        self.item_ref = item_ref

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
                                     command=self.main_frame.destroy)
        self.back_button.grid(row=0, column=0, pady=5, padx=10, sticky='w')

        self.label = CTkLabel(self.top_frame, text="Edit Entry", font=('Lato', 30))
        self.label.grid(row=0, column=1, pady=5, padx=10, sticky='w')

        self.separator = CTkLabel(self.main_frame, text='', bg_color='gray', height=1, font=('Arial', 2))
        self.separator.pack(fill='x', padx=10)
        
        # ===== Edit Values ===== #

        self.edit_main_frame = CTkFrame(self.main_frame, fg_color='transparent')
        self.edit_main_frame.pack(anchor='center', fill='both', pady=25, padx=15)

        self.edit_left_frame = CTkFrame(self.edit_main_frame)
        self.edit_left_frame.grid(row=0, column=0, sticky='nsew', pady=10)

        self.edit_mid_frame = CTkFrame(self.edit_main_frame)
        self.edit_mid_frame.grid(row=0, column=1, sticky='nsew', pady=10)

        # ===== Date ===== #

        self.date_frame = CTkFrame(self.edit_left_frame, fg_color='transparent')
        self.date_frame.grid(row=0, column=0, sticky='w', pady=10)

        self.date_label = CTkLabel(self.date_frame, text="Date", font=('Lato', 20))
        self.date_label.grid(row=0, column=0, sticky='w')

        self.date_entry = CTkEntry(self.date_frame, font=('Lato', 20), placeholder_text='Enter date (DD-MM-YYYY)')
        self.date_entry.insert(0, self.item_ref.date)
        self.date_entry.grid(row=1, column=0, sticky='w')

        self.date_hint_label = CTkLabel(self.date_frame, text="format: DD-MM-YYYY", font=('Lato', 12))
        self.date_hint_label.grid(row=2, column=0, sticky='w', pady=3)

        # ===== Desc ===== #

        self.desc_frame = CTkFrame(self.edit_left_frame, fg_color='transparent')
        self.desc_frame.grid(row=1, column=0, sticky='w', pady=10)

        self.desc_label = CTkLabel(self.desc_frame, text="Description", font=('Lato', 20))
        self.desc_label.grid(row=0, column=0, sticky='w')

        self.desc_entry = CTkTextbox(self.desc_frame, font=('Lato', 20), width=450, height=100)
        self.desc_entry.insert(END, self.item_ref.desc)
        self.desc_entry.grid(row=1, column=0, sticky='w')

        # ===== Component ===== #

        self.component_frame = CTkFrame(self.edit_left_frame, fg_color='transparent')
        self.component_frame.grid(row=2, column=0, sticky='w', pady=10)

        self.component_label = CTkLabel(self.component_frame, text="Parent Component", font=('Lato', 20))
        self.component_label.grid(row=0, column=0, sticky='w')

        self.component_menu = CTkOptionMenu(self.component_frame,
                                            values=[comp.name for comp in
                                                    self.root.app_session.selected_car.get_all_components()])
        self.component_menu.set(self.item_ref.component.name)
        self.component_menu.grid(row=1, column=0, sticky='w')

        # ===== Category ===== #

        self.category_frame = CTkFrame(self.edit_left_frame, fg_color='transparent')
        self.category_frame.grid(row=3, column=0, sticky='w', pady=10)

        self.category_label = CTkLabel(self.category_frame, text="Category", font=('Lato', 20))
        self.category_label.grid(row=0, column=0, sticky='w')

        self.category_menu = CTkOptionMenu(self.category_frame,
                                           values=[e for e in EntryCategory])
        self.category_menu.set(self.item_ref.category)
        self.category_menu.grid(row=1, column=0, sticky='w')

        # ===== Mileage ===== #

        self.mileage_frame = CTkFrame(self.edit_left_frame, fg_color='transparent')
        self.mileage_frame.grid(row=4, column=0, sticky='w', pady=10)

        self.mileage_label = CTkLabel(self.mileage_frame, text="Mileage", font=('Lato', 20))
        self.mileage_label.grid(row=0, column=0, sticky='w')

        self.mileage_entry = CTkEntry(self.mileage_frame, font=('Lato', 20), placeholder_text='Enter mileage (km)')
        self.mileage_entry.insert(0, self.item_ref.mileage)
        self.mileage_entry.grid(row=1, column=0, sticky='w')

        self.mileage_unit_label = CTkLabel(self.mileage_frame, text="km", font=('Lato', 20))
        self.mileage_unit_label.grid(row=1, column=1, sticky='w', padx=10)

        # ===== Custom Info ===== #

        self.custom_frame = CTkScrollableFrame(self.edit_mid_frame, fg_color='transparent', width=550, height=800)
        self.custom_frame.grid(row=0, column=0, sticky='w', pady=10, padx=100)

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
                                                    self.item_ref,
                                                    width=250)
        self.property_container.grid(row=1, column=0, columnspan=5, sticky='w')

        self.property_container.create_properties()

    def add_new_property(self):
        self.property_container.add_property()


class PropertyContainer(CTkFrame):
    def __init__(self, master, root: CTk, item_ref, **values):
        super().__init__(master, **values)
        self.master = master
        self.root = root
        self.item_ref = item_ref

        self.properties: dict[str, ...] = item_ref.custom_info
        self.property_widgets: list[PropertyItem] = []

    def add_property(self, name: str = 'New Property', value='Enter value'):
        new_item = PropertyItem(self, self.root, name, value, len(self.properties))
        self.property_widgets.append(new_item)

    def create_properties(self):
        for p in self.properties.items():
            self.add_property(p[0], p[1])


class PropertyItem:
    def __init__(self, master, root: CTk, property_name: str, property_value, index: int):
        self.master = master
        self.root = root

        self.index: int = index

        self.property_name: str = property_name
        self.property_value = property_value

        # ===== Widget ===== #

        self.property_frame = CTkFrame(self.master, fg_color='gray', width=400)
        self.property_frame.pack(fill='x', anchor='w', padx=2, pady=2)

        self.property_name_label = CTkEntry(self.property_frame, font=('Lato', 17), width=200)
        self.property_name_label.insert(0, self.property_name.capitalize())
        self.property_name_label.grid(row=0, column=0, sticky='w', padx=3, pady=2)

        self.separator = CTkLabel(self.property_frame,
                                  text='',
                                  bg_color='lightgray',
                                  height=20,
                                  width=3,
                                  font=('Arial', 2))
        self.separator.grid(row=0, column=1, sticky='w', padx=10)

        self.property_value_label = CTkEntry(self.property_frame, font=('Lato', 17), width=300)
        self.property_value_label.insert(0, self.property_value)
        self.property_value_label.grid(row=0, column=2, sticky='w', padx=3, pady=2)
