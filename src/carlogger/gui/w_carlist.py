from customtkinter import CTkFrame, CTkLabel, CTkButton

from carlogger.gui.const_gui import car_icon, get_img_from_path


class CarCard(CTkFrame):
    image = car_icon

    def __init__(self, master, car, row=0, col=0, **values):
        super().__init__(master, **values)
        self.master: CarFrame = master
        self.car = car

        self.row = row
        self.column = col

        # ===== Widget ===== #

        self.inner_frame = CTkFrame(self.master, fg_color='gray')
        self.inner_frame.grid(row=self.row, column=self.column, padx=5, pady=5)

        self.name = CTkLabel(self.inner_frame,
                             text=self.car.car_info.name, )

        self.name.grid(row=0, column=0)

        self.button = CTkButton(self.inner_frame,
                                fg_color='transparent',
                                bg_color='gray',
                                hover_color='lightgray',
                                width=250,
                                height=175,
                                text='',
                                command=self.go_to_car,
                                image=self.get_item_image())
        self.button.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    def get_item_image(self):
        if img := self.car.custom_info.get('image'):
            return get_img_from_path(img)
        else:
            return self.image

    def go_to_car(self):
        self.master.go_to_car(self.car)


class DummyCarCard(CTkFrame):
    def __init__(self, master, car, row=0, col=0, **values):
        super().__init__(master, **values)
        self.master: CarFrame = master
        self.car = car

        self.row = row
        self.column = col

        # ===== Widget ===== #

        self.inner_frame = CTkFrame(self.master, fg_color='transparent')
        self.inner_frame.grid(row=self.row, column=self.column, padx=5, pady=5)

        self.name = CTkLabel(self.inner_frame,
                             text='+',
                             font=('Lato', 15))

        self.name.grid(row=0, column=0)

        self.button = CTkButton(self.inner_frame,
                                fg_color='#323131',
                                border_color='lightgray',
                                border_width=3,
                                border_spacing=5,
                                hover_color='lightgray',
                                width=250,
                                height=210,
                                text='+',
                                font=('Lato', 50),
                                command=self.open_add_menu)
        self.button.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

    def open_add_menu(self):
        self.master.open_add_car_menu()


class CarFrame(CTkFrame):
    def __init__(self, master, root, **values):
        super().__init__(master, **values)
        self.root = root
        self.car_cards: list[CarCard] = []

        new_car_card = DummyCarCard(master=self, car=None, row=0, col=0)
        new_car_card.grid(row=0, column=0, sticky='w')
        self.car_cards.append(new_car_card)

    def add_car(self, car):
        col = len(self.car_cards)
        new_car_card = CarCard(master=self, car=car, row=0, col=col)
        new_car_card.grid(row=0, column=col, sticky='w')
        self.car_cards.append(new_car_card)

    def clear_cars(self):
        for child in self.car_cards:
            child.destroy()

        self.car_cards = []

    def go_to_car(self, car):
        self.root.go_to_car(car)

    def open_add_car_menu(self):
        self.root.open_car_add_window()
