from customtkinter import CTk


class RootWindow(CTk):
    def __init__(self):
        super().__init__()
        self.app_session = None

        self.title("Carlogger")
        self.geometry("500x400")

    def start_mainloop(self):
        self.mainloop()
