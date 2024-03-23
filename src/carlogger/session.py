"""Class that combines everything together, the heart of the program"""

from carlogger.directory_manager import DirectoryManager
from carlogger.car import Car
from carlogger.car_info import CarInfo
from carlogger.arg_executor import ArgExecutor, AddArgExecutor, ReadArgExecutor, DeleteArgExecutor


class AppSession:
    """Setup current app session, load saved info: load collections, components and log entries."""
    def __init__(self, directory_manager: DirectoryManager):
        self.directory_manager = directory_manager

        self.cars: list[Car] = []
        self.selected_car: Car = ...

        self.arg_executor: ArgExecutor = ...

    def execute_console_args(self, subparser_type: str, parsed_args: dict, raw_args: list[str]):
        """Create ArgExecutor object based on subparser in use and execute console arguments."""
        match subparser_type:
            case 'read':
                self.arg_executor = ReadArgExecutor(parsed_args, self)
            case 'add':
                self.arg_executor = AddArgExecutor(parsed_args, self, raw_args)
            case 'delete':
                self.arg_executor = DeleteArgExecutor(parsed_args, self, raw_args)
            case _:
                return

        self.arg_executor.evaluate_args()

    def add_new_car(self, car_info: dict) -> Car:
        """Create a new car directory."""
        car_info = CarInfo(**car_info)
        new_car = Car(car_info)
        car_info.path = self.directory_manager.create_car_info_path(new_car)

        self.cars.append(new_car)
        self.directory_manager.create_car_directory(new_car)

        self.selected_car = self.cars[0]

        return new_car

    def delete_car(self, car_name: str):
        """Delete car directory by name."""
        car_to_remove = self.get_car_by_name(car_name)
        self.directory_manager.remove_car_directory(car_to_remove)
        self.cars.remove(car_to_remove)

    def save_car(self, car_name: str):
        """Update car directory."""
        car = self.get_car_by_name(car_name)
        self.directory_manager.update_car_directory(car)

    def add_new_collection(self, car_name: str, collection_name: str):
        """Add new collection to specified car and update save directory."""
        car = self.get_car_by_name(car_name)
        car.create_collection(collection_name)
        self.directory_manager.update_car_directory(car)

    def delete_collection(self, car_name: str, collection_name: str):
        """Delete collection from target car by name."""
        car = self.get_car_by_name(car_name)
        car.delete_collection(collection_name)
        self.directory_manager.update_car_directory(car)

    def add_new_component(self, car_name: str, collection_name: str, component_name: str):
        """Add new collection to specified car and update save directory."""
        car = self.get_car_by_name(car_name)
        collection = car.get_collection_by_name(collection_name)
        collection.create_component(component_name)
        self.directory_manager.update_car_directory(car)

    def delete_component(self, car_name: str, collection_name: str, component_name: str):
        """Delete component by name from target collection from specified car."""
        car = self.get_car_by_name(car_name)
        coll = car.get_collection_by_name(collection_name)
        coll.delete_component(component_name)
        self.directory_manager.update_car_directory(car)

    def add_new_entry(self, car_name: str, collection_name: str, component_name: str, entry_data: dict):
        """Add new collection to specified car and update save directory."""
        car = self.get_car_by_name(car_name)
        collection = car.get_collection_by_name(collection_name)
        component = collection.get_component_by_name(component_name)
        component.create_entry(entry_data)
        self.directory_manager.update_car_directory(car)

    def delete_entry_by_index(self, car_name: str, component_name: str, entry_index: int):
        """Delete entry via list index from target component."""
        car = self.get_car_by_name(car_name)
        comp = car.get_component_by_name(component_name)
        comp.remove_entry_by_index(entry_index)
        self.directory_manager.update_car_directory(car)

    def delete_entry_by_id(self, car_name: str, component_name: str, entry_id: str):
        """Delete entry via list index from target component."""
        car = self.get_car_by_name(car_name)
        comp = car.get_component_by_name(component_name)
        comp.remove_entry_by_id(entry_id)
        self.directory_manager.update_car_directory(car)

    def get_car_by_name(self, car_name: str) -> Car:
        """Find car by name. If it's not found, attempt loading the car from save directory and check again."""
        try:
            return list(filter(lambda x: x.car_info.name == car_name, self.cars))[0]
        except IndexError:
            return self.load_car_dir(car_name)

    def load_car_dir(self, car_name: str) -> Car:
        """Load a singular car directory and add it to the list.\n
        Loads directory only if the specified car wasn't requested prior, else find the car instance and return it"""
        car = self.directory_manager.load_car_dir(car_name)
        self.cars.append(car)
        self.selected_car = car
        return car
