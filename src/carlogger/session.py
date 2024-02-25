"""Class that combines everything together, the heart of the program"""

from carlogger.car import Car


class AppSession:
    """Setup current app session, load saved info: load collections, components and log entries."""
    def __init__(self, cars: list[Car] = None):
        self.cars: list[Car] = cars
        self.selected_car: Car = self.cars[0] or None
