from customtkinter import CTkFrame, CTkButton

from carlogger.gui.c_itemlist import ItemList
from carlogger.gui.w_itemlist import ItemContainer


class Homepage(CTkFrame):
    def __init__(self, master, root, **kwargs):
        super().__init__(master,
                         corner_radius=0,
                         fg_color="transparent",
                         **kwargs)
        self.master = master
        self.root = root

        self.grid(row=0, column=0, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.item_container = ItemContainer(self, parent_car=None, root=self.root, homepage=True)
        self.item_container.grid(row=1, column=0, sticky="nsew")

        self.item_list = ItemList(self, widget=self.item_container, app_session=self.root.app_session)

    def create_items(self, items, parent_car, header, sort_key: str = '*'):
        self.item_container.parent = self.item_list
        self.item_container.parent_car = parent_car
        self.item_container.app_session = self.root.app_session
        self.item_list.create_items(items, header, sort_key)

    def homepage_init(self):
        if self.root.cars:
            self.create_items(self._get_all_scheduled_entries()[:5:],
                              self.root.cars[0],
                              'Scheduled Log Entries',
                              'oldest')
            self.create_items(self._get_all_log_entries()[:5:],
                              self.root.cars[0],
                              'Log Entries')

    def _get_all_scheduled_entries(self) -> list:
        cars = self.root.cars
        scheduled_entries = [car.get_all_scheduled_entry_logs() for car in cars]

        se = []
        [se.extend(entry_list) for entry_list in scheduled_entries]

        return se

    def _get_all_log_entries(self) -> list:
        cars = self.root.cars
        log_entries = [car.get_all_entry_logs() for car in cars]

        le = []
        [le.extend(entry_list) for entry_list in log_entries]

        return le

