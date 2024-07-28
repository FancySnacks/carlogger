from customtkinter import CTkEntry, CTkFrame, CTkLabel, StringVar

from carlogger.gui.const_gui import search_icon_mini


class Searchbar:
    def __init__(self, master, root):
        self.master = master
        self.root = root

        self.search_var = StringVar(value='')
        self.search_var.trace_add('write', self.track_changes)

        self.main_frame = CTkFrame(master=self.master, fg_color='transparent')
        self.main_frame.pack(expand=False, side='right', padx=10, pady=5)

        self.search_img = CTkLabel(master=self.main_frame, image=search_icon_mini, text='')
        self.search_img.pack(expand=False, side='left', padx=10)

        self.search_bar = CTkEntry(master=self.main_frame,
                                   placeholder_text="Search",
                                   textvariable=self.search_var,
                                   width=200,
                                   height=30,
                                   font=('Lato', 17))
        self.search_bar.pack(expand=True, fill='x')

    def track_changes(self, *args):
        self.search_var.get()


class SearchResult:
    def __init__(self):
        pass
