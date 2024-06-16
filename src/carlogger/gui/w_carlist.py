from customtkinter import CTkFrame, CTkLabel, CTkButton


class CarCard(CTkFrame):
    def __init__(self, master, car, **values):
        super().__init__(master, **values)
        self.master: CarFrame = master
        self.car = car

        self.column = 0
        self.row = 0

        # ===== Widget ===== #

        self.inner_frame = CTkFrame(self.master,
                                    fg_color='gray')
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
                                command=self.go_to_car)
        self.button.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    def go_to_car(self):
        self.master.go_to_car(self.car)


class CarFrame(CTkFrame):
    def __init__(self, master, root, **values):
        super().__init__(master, **values)
        self.root = root
        self.car_cards: list[CarCard] = []

    def add_car(self, car):
        new_car_card = CarCard(master=self, car=car)
        new_car_card.grid(row=0, column=len(self.car_cards), sticky='w')
        self.car_cards.append(new_car_card)

    def clear_cars(self):
        for child in self.car_cards:
            child.destroy()

        self.car_cards = []

    def go_to_car(self, car):
        self.root.go_to_car(car)
