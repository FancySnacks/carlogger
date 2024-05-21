from customtkinter import CTkScrollableFrame


class Frame(CTkScrollableFrame):
    def __init__(self, master, **values):
        super().__init__(master, **values)
