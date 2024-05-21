from customtkinter import CTkFrame, CTkButton, CTkLabel


class NavigationBar(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.main_frame = CTkFrame(master=self, height=150, fg_color='red')
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Configure grid for centering
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(3, weight=0)
        self.main_frame.grid_columnconfigure(5, weight=0)
        self.main_frame.grid_columnconfigure(6, weight=1)

        self.button = CTkButton(master=self.main_frame, text="CarTestPytest", width=100, height=30, font=('Lato', 17))
        self.button.grid(row=0, column=1, padx=5, pady=5)

        self.label = CTkLabel(master=self.main_frame, text=">", font=('Lato', 22))
        self.label.grid(row=0, column=2, padx=15, pady=5)

        self.button2 = CTkButton(master=self.main_frame, text="Engine", width=100, height=30, font=('Lato', 17))
        self.button2.grid(row=0, column=3, padx=5, pady=5)

        self.label = CTkLabel(master=self.main_frame, text=">", font=('Lato', 22))
        self.label.grid(row=0, column=4, padx=15, pady=5)

        self.button3 = CTkButton(master=self.main_frame,
                                 text="Spark Plug",
                                 width=100,
                                 height=30,
                                 font=('Lato', 21),
                                 border_spacing=5)
        self.button3.grid(row=0, column=5, padx=5, pady=5)
