from customtkinter import CTk

from carlogger.gui.w_frame import Frame
from carlogger.gui.c_carlist import CarList
from carlogger.gui.w_carframe import CarFrame
from carlogger.gui.w_navigation import NavigationBar
from carlogger.gui.w_itemlist import ItemContainer
from carlogger.gui.c_itemlist import ItemList
from carlogger.gui.w_editentry import EditEntryPopup


class RootWindow(CTk):
    def __init__(self):
        super().__init__()
        self.app_session = None

        self.title('Carlogger')
        self.geometry("1000x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = Frame(master=self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, weight=1)

        self.navigation = NavigationBar(master=self.main_frame)
        self.navigation.grid(row=0, column=0, sticky='ew')

        self.car_frame = CarFrame(self.main_frame)
        self.car_frame.grid(row=1, column=0, sticky='nsew')

        self.car_list = CarList(self.car_frame)

        self.item_container = ItemContainer(self.main_frame, parent_car=None, root=self)
        self.item_container.grid(row=2, column=0, sticky="nsew")

        self.item_list = None

    def start_mainloop(self):
        self.mainloop()

    def create_items(self, items, parent, header):
        self.item_list = ItemList(parent, widget=self.item_container, app_session=self.app_session)
        self.item_container.parent = self.item_list
        self.item_container.app_session = self.app_session
        self.item_container.parent_car = parent
        self.item_list.create_items(items, header)

    def reset_item_list_widget(self):
        self.item_container.collapse_widget()

    def open_entry_edit_window(self, item_ref):
        self.edit_entry_popup = EditEntryPopup(self.main_frame, self, item_ref)
