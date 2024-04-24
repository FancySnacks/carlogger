"""Class that combines everything together, the heart of the program"""

from carlogger.directory_manager import DirectoryManager
from carlogger.items.car import Car
from carlogger.items.car_info import CarInfo
from carlogger.cli.arg_executor import ArgExecutor, AddArgExecutor, ReadArgExecutor, DeleteArgExecutor, \
    UpdateArgExecutor
from carlogger.items.component_collection import ComponentCollection


class AppSession:
    """Setup current app session, load saved info: load collections, components and log entries."""
    def __init__(self, directory_manager: DirectoryManager):
        self.directory_manager = directory_manager
        self.arg_executor: ArgExecutor = ...

        self.cars: list[Car] = []
        self.selected_car: Car = ...

    def execute_console_args(self, subparser_type: str, parsed_args: dict, raw_args: list[str]):
        """Create ArgExecutor object based on subparser in use and execute console arguments."""
        match subparser_type:
            case 'read':
                self.arg_executor = ReadArgExecutor(parsed_args, self, raw_args)
            case 'add':
                self.arg_executor = AddArgExecutor(parsed_args, self, raw_args)
            case 'delete':
                self.arg_executor = DeleteArgExecutor(parsed_args, self, raw_args)
            case 'update':
                self.arg_executor = UpdateArgExecutor(parsed_args, self, raw_args)
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

    def add_new_nested_collection(self, car_name: str, collection_name: str, parent_collection_name: str):
        """Add new nested collection to specified car and parent collection and update save directory."""
        car = self.get_car_by_name(car_name)
        car.create_nested_collection(collection_name, parent_collection_name)
        self.directory_manager.update_car_directory(car)

    def delete_collection(self, car_name: str, collection_name: str):
        """Delete collection from target car by name."""
        car = self.get_car_by_name(car_name)
        coll = car.get_collection_by_name(collection_name)

        if coll and len(coll.children) > 0:
            self.delete_collection_children(coll, car_name)

        self.directory_manager.remove_item(coll)
        car.delete_collection(collection_name)
        self.directory_manager.update_car_directory(car)

    def delete_collection_children(self, collection: ComponentCollection, car_name: str):
        for ch in collection.children:
            if type(ch) == ComponentCollection:
                self.delete_collection(car_name, ch.name)
            else:
                self.delete_component(car_name, collection.name, ch.name)
        collection.delete_children()

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
        comp = coll.get_component_by_name(component_name)
        self.directory_manager.remove_item(comp)
        coll.delete_component(component_name)
        self.directory_manager.update_car_directory(car)

    def add_new_entry(self, car_name: str, collection_name: str, component_name: str, entry_data: dict):
        """Add new entry to specified car and update save directory."""
        car = self.get_car_by_name(car_name)
        collection = car.get_collection_by_name(collection_name)
        component = collection.get_component_by_name(component_name)
        component.create_entry(entry_data)
        self.directory_manager.update_car_directory(car)

    def add_new_scheduled_entry(self, car_name: str, collection_name: str, component_name: str, entry_data: dict):
        """Add new collection to specified car and update save directory."""
        car = self.get_car_by_name(car_name)
        collection = car.get_collection_by_name(collection_name)
        component = collection.get_component_by_name(component_name)
        component.create_scheduled_entry(entry_data)
        self.directory_manager.update_car_directory(car)

    def delete_entry_by_index(self, car_name: str, component_name: str, entry_index: int):
        """Delete entry via list index from target component."""
        car = self.get_car_by_name(car_name)
        comp = car.get_component_by_name(component_name)
        comp.delete_entry_by_index(entry_index)
        self.directory_manager.update_car_directory(car)

    def delete_entry_by_id(self, car_name: str, entry_id: str):
        """Delete entry via list index from target component."""
        car = self.get_car_by_name(car_name)
        comp = car.get_component_of_entry_by_entry_id(entry_id)
        comp.delete_entry_by_id(entry_id)
        self.directory_manager.update_car_directory(car)

    def update_car_info(self, car: Car, updated_data: dict[str, ...]):
        """Update target car info values and update the save file."""

        legacy_car_info_path = car.car_info.path

        for key, value in updated_data.items():
            setattr(car.car_info, key, value)

        # Create new directory and copy items over when changing name of the car
        if 'name' in updated_data.keys():
            self.directory_manager.rename_car_dir(car, legacy_car_info_path)
        else:
            self.directory_manager.update_car_directory(car)

    def update_component_or_collection(self, parent_car: Car, item, updated_data: dict[str, ...]):
        self.directory_manager.remove_item(item)

        for key, value in updated_data.items():
            setattr(item, key, value)

        self.directory_manager.update_car_directory(parent_car)

    def update_entry(self, parent_car: Car, entry, updated_data: dict[str, ...]):
        """Update values of target entry and update the save file."""
        for key, value in updated_data.items():
            setattr(entry, key, value)

        self.directory_manager.update_car_directory(parent_car)

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
