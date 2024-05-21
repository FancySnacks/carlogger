from customtkinter import CTk

from carlogger.gui.w_frame import Frame
from carlogger.gui.c_carlist import CarList
from carlogger.gui.w_carframe import CarFrame
from carlogger.gui.w_navigation import NavigationBar


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

    def start_mainloop(self):
        self.mainloop()
