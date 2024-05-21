class CarList:
    def __init__(self, widget):
        self.widget = widget
        self.widget.grid(row=0, column=0, sticky="nsew")
        self.cars: list = []

    def add_car(self, car):
        if not self._is_car_duplicate(car):
            self.cars.append(car)
            self.create_car_widget(car)

    def create_car_widget(self, car):
        self.widget.add_car(car)

    def _is_car_duplicate(self, car) -> bool:
        for c in self.cars:
            if c.car_info.name == car.car_info.name:
                return True

        return False
