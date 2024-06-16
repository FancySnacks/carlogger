from customtkinter import CTkFrame, CTkButton, CTkLabel


class NavigationBar(CTkFrame):
    def __init__(self, master, root, **kwargs):
        super().__init__(master, **kwargs)
        self.nav_widgets: list = []
        self.nav_items: list = []

        self.root = root

        self.current_item = None

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

    def add_nav_item(self, name: str, item_ref, **kwargs):
        self.nav_items.append(item_ref)
        self.current_item = self.nav_items[-1]

        if len(self.nav_widgets) % 2 != 0:
            self.add_separator()

        nav_item = NavItem(self,
                           widget_master=self.main_frame,
                           name=name,
                           id=len(self.nav_widgets),
                           item_ref=item_ref,
                           column=self._get_column())
        self.nav_widgets.append(nav_item)

    def add_separator(self):
        separator = Separator(self,
                              widget_master=self.main_frame,
                              id=len(self.nav_widgets),
                              column=self._get_column())
        self.nav_widgets.append(separator)

    def go_to_previous_page(self, nav_item):
        if nav_item.item_ref == self.current_item:
            return

        if len(self.nav_items) < 2:
            return

        item_index = nav_item.id

        for widget in self.nav_widgets[item_index + 1:]:
            widget.button.grid_forget() if isinstance(widget, NavItem) else widget.separator.grid_forget()
            widget.destroy()

        self.nav_widgets = self.nav_widgets[:item_index + 1]
        self.nav_items = self.nav_items[:(item_index // 2) + 1]
        self.current_item = self.nav_items[-1] if self.nav_items else None

        if not nav_item.item_ref:
            self.root.go_to_homepage()

    def _get_column(self) -> int:
        return len(self.nav_widgets) + 1


class NavItem(CTkButton):
    def __init__(self, master, widget_master, name: str, id: int, item_ref, column=1, page_ref=None, **kwargs):
        super().__init__(master, **kwargs)
        self.id = id
        self.item_ref = item_ref

        self.button = CTkButton(master=widget_master,
                                text=name,
                                width=100,
                                height=30,
                                font=('Lato', 17),
                                command=self.go_to_page,
                                **kwargs)
        self.button.grid(row=0, column=column, padx=5, pady=5)

    def go_to_page(self):
        self.master.go_to_previous_page(self)


class Separator(CTkLabel):
    def __init__(self, master, widget_master, id: int, column=1, page_ref=None, **kwargs):
        super().__init__(master, **kwargs)
        self.id = id

        self.separator = CTkLabel(master=widget_master, text=">", font=('Lato', 22))
        self.separator.grid(row=0, column=column, padx=15, pady=5)
