from customtkinter import CTkFrame, CTkLabel, CTkButton


class CarCard(CTkFrame):
    def __init__(self, master, car, **values):
        super().__init__(master, **values)
        self.master: CarFrame = master
        self.car = car

        self.main_frame = CTkFrame(master=self, corner_radius=5, fg_color="lightgray")
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.info_frame = CTkFrame(master=self.main_frame,
                                   corner_radius=0,
                                   fg_color="lightgray")
        self.info_frame.grid(row=0, column=0, sticky='nsew', padx=15, pady=3)

        self.button = CTkButton(master=self.main_frame,
                                corner_radius=0,
                                text=">",
                                width=15,
                                font=('Lato', 25),
                                command=self.go_to_car)
        self.button.grid(row=0, column=1, sticky='nsw')

        self.car_name_label = CTkLabel(master=self.info_frame,
                                       text=car.car_info.name,
                                       text_color='white',
                                       font=('Lato', 20),
                                       fg_color='transparent')
        self.car_name_label.grid(row=0, column=0, columnspan=5, sticky='w')

        self.car_model_label = CTkLabel(master=self.info_frame,
                                        text=f"{car.car_info.manufacturer} {car.car_info.model} "
                                             f"({car.car_info.year})",
                                        text_color='white',
                                        font=('Lato', 15),
                                        fg_color='transparent')
        self.car_model_label.grid(row=1, column=0, sticky='w')

        self.car_mileage_label = CTkLabel(master=self.info_frame,
                                          text=f"{car.car_info.mileage} km",
                                          text_color='white',
                                          font=('Lato', 15),
                                          fg_color='transparent')
        self.car_mileage_label.grid(row=2, column=0, sticky='w')

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
