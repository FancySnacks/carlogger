"""Class that combines everything together, the heart of the program"""

from carlogger.directory_manager import DirectoryManager
from carlogger.car import Car
from carlogger.car_info import CarInfo
from carlogger.arg_executor import ArgExecutor, AddArgExecutor, ReadArgExecutor


class AppSession:
    """Setup current app session, load saved info: load collections, components and log entries."""
    def __init__(self, directory_manager: DirectoryManager):
        self.directory_manager = directory_manager

        self.cars: list[Car] = []
        self.selected_car: Car = ...

        self.arg_executor: ArgExecutor = ...

    def execute_console_args(self, subparser_type: str, parsed_args: dict):
        """Create ArgExecutor object based on subparser in use and execute console arguments."""
        match subparser_type:
            case 'read':
                self.arg_executor = ReadArgExecutor(parsed_args, self)
            case 'add':
                self.arg_executor = AddArgExecutor(parsed_args, self)

        self.arg_executor.evaluate_args()

    def add_new_car(self, car_info: dict):
        """Create a new car directory."""
        car_info = CarInfo(**car_info)
        new_car = Car(car_info)
        car_info.path = self.directory_manager.create_car_info_path(new_car)

        self.cars.append(new_car)
        self.directory_manager.create_car_directory(new_car)

        self.selected_car = self.cars[0]

    def remove_car(self, car_name: str):
        """Delete car directory by name."""
        car_to_remove = self.find_car_by_name(car_name)
        self.directory_manager.remove_car_directory(car_to_remove)
        self.cars.remove(car_to_remove)

    def save_car(self, car_name: str):
        car = self.find_car_by_name(car_name)
        self.directory_manager.update_car_directory(car)

    def find_car_by_name(self, car_name: str) -> Car:
        return list(filter(lambda x: x.car_info.name == car_name, self.cars))[0]
