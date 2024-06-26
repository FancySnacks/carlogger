from customtkinter import CTk, CTkScrollbar, CTkFrame
from tkinter import Canvas

from carlogger.gui.w_editcar import EditCarPopup
from carlogger.gui.w_editcollection import EditCollectionPopup
from carlogger.gui.w_homepage import Homepage
from carlogger.gui.c_carlist import CarList
from carlogger.gui.w_carlist import CarFrame
from carlogger.gui.w_navigation import NavigationBar
from carlogger.gui.w_itemlist import ItemContainer
from carlogger.gui.c_itemlist import ItemList
from carlogger.gui.w_editentry import EditEntryPopup
from carlogger.gui.w_addentry import AddEntryPopup
from carlogger.gui.w_addcar import AddCarPopup
from carlogger.gui.w_addcollection import AddCollectionPopup
from carlogger.gui.w_addcomponent import AddComponentPopup
from carlogger.gui.w_collectionlist import CollectionContainer
from carlogger.gui.w_componentlist import ComponentContainer


class RootWindow(CTk):
    def __init__(self):
        super().__init__()
        self.app_session = None
        self.cars = []
        self.selected_car = None
        self.selected_collection = None
        self.current_page = None

        self.title('Carlogger')
        self.geometry("1000x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = CTkFrame(master=self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.navigation = NavigationBar(master=self.main_frame, root=self)
        self.navigation.grid(row=0, column=0, sticky='ew')

        # Create a canvas to allow for scrolling
        self.canvas = Canvas(self.main_frame,
                             bg="black",
                             background='black',
                             bd=0,
                             border=0,
                             borderwidth=0,
                             highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.scrollbar = CTkScrollbar(self.main_frame,
                                      orientation='vertical',
                                      command=self.canvas.yview,
                                      bg_color='transparent')
        self.scrollbar.grid(row=1, column=1, sticky='ns')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Bind mouse scroll to the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # For Linux systems
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # For Linux systems

        self.scrollable_frame = CTkFrame(self.canvas, corner_radius=0, fg_color="transparent")
        self.canvas.create_window((0.0, 0.0),
                                  window=self.scrollable_frame,
                                  anchor='nw',
                                  height=self.canvas.winfo_screenheight(),
                                  width=self.canvas.winfo_screenwidth())

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)

        self.navigation.add_nav_item('Home', None)

        self.car_list = None
        self.homepage = None

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

    def start_mainloop(self):
        self.go_to_homepage()
        self.mainloop()

    def reset_item_list_widget(self):
        self.homepage.item_container.collapse_widget()

    def create_items(self, items, parent_car, header, sort_key: str = '*'):
        self.homepage.create_items(items, parent_car, header, sort_key)

    def delete_entries(self, entries: list):
        car_name = self.selected_car.car_info.name
        component = entries[0].component
        entry_ids = [entry.id for entry in entries]

        if len(entry_ids) == 1:
            self.app_session.delete_entry_by_id(car_name, entry_ids[0], component)
        else:
            self.app_session.delete_entries_by_id(car_name, entry_ids)

    def open_entry_edit_window(self, item_ref, item_widget):
        self.edit_entry_popup = EditEntryPopup(self.main_frame, self, item_ref, item_widget)

    def open_entry_add_window(self, item_container, scheduled_entry: bool = False):
        self.add_entry_popup = AddEntryPopup(self.main_frame,
                                             self,
                                             item_container,
                                             parent_component=self.navigation.current_item,
                                             scheduled_entry=scheduled_entry)

    def open_car_add_window(self):
        self.add_car_popup = AddCarPopup(self.main_frame, self)

    def open_collection_add_window(self):
        self.add_collection_popup = AddCollectionPopup(self.main_frame, self, self.selected_car)

    def open_component_add_window(self):
        self.add_component_popup = AddComponentPopup(self.main_frame, self, self.selected_collection, self.selected_car)

    def open_car_edit_window(self):
        self.edit_car_popup = EditCarPopup(self.main_frame, self, self.selected_car)

    def open_collection_edit_window(self):
        self.edit_car_popup = EditCollectionPopup(self.main_frame, self, self.selected_car, self.selected_collection)

    def open_component_edit_window(self):
        print("[TO IMPLEMENT] RootWindow: open_component_edit_window()")

    def create_cars(self):
        self.car_list.clear_cars()

        for car in self.cars:
            self.car_list.add_car(car)

    def go_to_homepage(self):
        self.homepage = Homepage(self.scrollable_frame, self)

        car_frame = CarFrame(self.homepage, self)
        car_frame.grid(row=0, column=0, sticky='nsew')

        if self.current_page:
            self.current_page.destroy()
        self.current_page = car_frame

        if not self.car_list:
            self.car_list = CarList(car_frame)
        else:
            self.car_list.widget = car_frame

        self.create_cars()
        self.homepage.homepage_init()

    def go_to_car(self, car):
        collection_container = CollectionContainer(self.scrollable_frame,
                                                   root=self,
                                                   go_to_func=self.go_to_collection,
                                                   add_widget_func=self.open_collection_add_window)
        collection_container.create_items(car.collections)

        self.open_page(collection_container, car.car_info.name, car)
        self.selected_car = car

    def go_to_collection(self, collection):
        self.selected_collection = collection

        component_container = ComponentContainer(self.scrollable_frame,
                                                 root=self,
                                                 go_to_func=self.go_to_component,
                                                 add_widget_func=self.open_component_add_window)
        component_container.create_items(collection.components)

        self.open_page(component_container, collection.name, collection)

    def go_to_component(self, component):
        item_container = ItemContainer(self.scrollable_frame, parent_car=None, root=self, component=component)
        item_container.grid(row=0, column=0, sticky="nsew")

        item_list = ItemList(self.scrollable_frame, widget=item_container, app_session=self.app_session)

        item_container.parent = item_list
        item_container.app_session = self.app_session

        item_list.create_items(component.scheduled_log_entries, 'Scheduled Log Entries', 'oldest')
        item_list.create_items(component.log_entries, 'Log Entries', 'latest')

        self.open_page(item_container, component.name, component)

    def open_page(self, new_page, name, item_ref):
        if self.current_page:
            self.current_page.destroy()

        self.current_page = new_page
        self.navigation.add_nav_item(name, item_ref)
