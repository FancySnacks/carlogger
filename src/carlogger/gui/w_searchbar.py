from customtkinter import CTkButton, CTkFrame

from carlogger.gui.const_gui import search_icon_mini


class Searchbar:
    def __init__(self, master, root):
        self.master = master
        self.root = root

        self.main_frame = CTkFrame(master=self.master, fg_color='transparent')
        self.main_frame.pack(padx=5, pady=5)

        self.button = CTkButton(master=self.main_frame,
                                text='Search',
                                width=100,
                                height=30,
                                image=search_icon_mini,
                                font=('Lato', 17))
        self.button.pack(padx=5, pady=5)
