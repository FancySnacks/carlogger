from customtkinter import CTkLabel, CTkButton, CTkFrame


class DeletionConfirmation:
    def __init__(self, master, root, item_ref, delete_func):
        self.master = master
        self.root = root
        self.item_ref = item_ref
        self.delete_func = delete_func

        # ===== Overlay Frame ===== #

        self.overlay_frame = CTkFrame(self.master, bg_color='transparent')
        self.overlay_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ===== Main Popup Frame ===== #

        self.popup_frame = CTkFrame(self.master, width=400, height=225, corner_radius=10, bg_color='transparent')
        self.popup_frame.place(relx=0.5, rely=0.5, anchor='center')

        # ===== Widget ===== #

        self.main_frame = CTkFrame(self.popup_frame)
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.top_frame = CTkFrame(self.main_frame, fg_color='transparent')
        self.top_frame.pack(anchor='center')

        self.label = CTkLabel(self.top_frame, text="Are you sure?", font=('Lato', 22))
        self.label.grid(row=0, column=0, pady=5, padx=10, sticky='w')

        self.back_button = CTkButton(self.top_frame,
                                     text="X",
                                     font=('Lato', 30),
                                     width=5,
                                     corner_radius=0,
                                     anchor='center',
                                     fg_color='transparent',
                                     command=self.close_menu)
        self.back_button.grid(row=0, column=1, sticky='e')

        self.separator = CTkLabel(self.top_frame, text='', bg_color='gray', height=1, font=('Arial', 2))
        self.separator.grid(row=1, column=0, sticky='nsew')

        self.add_main_frame = CTkLabel(self.top_frame,
                                       text=f"You will delete '{self.item_ref.name}' and it's "
                                            f"{len(self.item_ref.children)} children.",
                                       font=('Lato', 20))
        self.add_main_frame.grid(row=2, column=0, pady=5, padx=10, sticky='w')

        self.confirm_frame = CTkFrame(self.main_frame, fg_color='transparent')
        self.confirm_frame.pack(fill='x', padx=10, pady=50)

        self.delete_button = CTkButton(self.confirm_frame,
                                       text="Delete",
                                       font=('Lato', 20),
                                       fg_color='red',
                                       corner_radius=10,
                                       command=self.confirm_deletion)
        self.delete_button.grid(row=0, column=1, sticky='w', padx=15, pady=5)

        self.cancel_button = CTkButton(self.confirm_frame,
                                       text="Cancel",
                                       font=('Lato', 20),
                                       corner_radius=10,
                                       command=self.close_menu)
        self.cancel_button.grid(row=0, column=2, sticky='e', padx=15, pady=5)

    def confirm_deletion(self):
        self.delete_func()
        self.close_menu()

    def close_menu(self, *args):
        self.overlay_frame.destroy()
        self.popup_frame.destroy()
        del self
