from customtkinter import CTk

from carlogger.gui.w_frame import Frame
from carlogger.gui.c_carlist import CarList
from carlogger.gui.w_carframe import CarFrame

class RootWindow(CTk):
    def __init__(self):
        super().__init__()
        self.app_session = None

        self.title('Carlogger')
        self.geometry("1000x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = Frame(master=self, width=700, height=1000, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.car_list = CarList(CarFrame(self.main_frame, width=700, height=1000))

    def start_mainloop(self):
        self.mainloop()
