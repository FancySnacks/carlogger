from customtkinter import CTk, CTkScrollbar, CTkFrame
from tkinter import Canvas

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

        self.main_frame = CTkFrame(master=self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.navigation = NavigationBar(master=self.main_frame)
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
                                  width=self.canvas.winfo_screenwidth())

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)

        self.car_frame = CarFrame(self.scrollable_frame)
        self.car_frame.grid(row=0, column=0, sticky='nsew')

        self.car_list = CarList(self.car_frame)

        self.item_container = ItemContainer(self.scrollable_frame, parent_car=None, root=self)
        self.item_container.grid(row=1, column=0, sticky="nsew")

        self.item_list = None

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

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
