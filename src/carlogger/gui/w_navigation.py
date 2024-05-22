from customtkinter import CTkFrame, CTkButton, CTkLabel


class NavigationBar(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.nav_items: list = []

        self.main_frame = CTkFrame(master=self, height=150, fg_color='red')
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=0)
        self.main_frame.grid_columnconfigure(3, weight=0)
        self.main_frame.grid_columnconfigure(4, weight=0)
        self.main_frame.grid_columnconfigure(5, weight=0)
        self.main_frame.grid_columnconfigure(6, weight=0)
        self.main_frame.grid_columnconfigure(7, weight=0)
        self.main_frame.grid_columnconfigure(8, weight=1)

        self.add_nav_item('Home')
        self.add_nav_item('CarTestPytest')
        self.add_nav_item('Engine')
        self.add_nav_item('Spark Plug')

    def add_nav_item(self, name: str, **kwargs):
        if len(self.nav_items) % 2 != 0:
            self.add_separator()

        nav_item = NavItem(self,
                           widget_master=self.main_frame,
                           name=name,
                           id=len(self.nav_items),
                           column=self._get_column())
        self.nav_items.append(nav_item)

    def add_separator(self):
        separator = Separator(self,
                              widget_master=self.main_frame,
                              id=len(self.nav_items),
                              column=self._get_column())
        self.nav_items.append(separator)

    def go_to_previous_page(self, nav_item):
        items_to_remove = self.nav_items[nav_item.id+1::]
        indexes_to_remove = [item.id for item in items_to_remove]

        for child in self.main_frame.winfo_children():
            if self.main_frame.winfo_children().index(child) in indexes_to_remove:
                child.destroy()

        self.nav_items = self.nav_items[0:nav_item.id+1:]
        self.master.update_idletasks()

    def _get_column(self) -> int:
        return len(self.nav_items) + 1


class NavItem(CTkButton):
    def __init__(self, master, widget_master, name: str, id: int, column=1, page_ref=None, **kwargs):
        super().__init__(master, **kwargs)
        self.id = id

        self.button3 = CTkButton(master=widget_master,
                                 text=name,
                                 width=100,
                                 height=30,
                                 font=('Lato', 17),
                                 command=self.go_to_page,
                                 **kwargs)
        self.button3.grid(row=0, column=column, padx=5, pady=5)

    def go_to_page(self):
        self.master.go_to_previous_page(self)


class Separator(CTkButton):
    def __init__(self, master, widget_master, id: int, column=1, page_ref=None, **kwargs):
        super().__init__(master, **kwargs)
        self.id = id

        self.separator = CTkLabel(master=widget_master, text=">", font=('Lato', 22))
        self.separator.grid(row=0, column=column, padx=15, pady=5)
