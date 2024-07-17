"""Class that combines everything together, the heart of the program"""
import os

from pathlib import Path

from carlogger.gui.root_window import RootWindow
from carlogger.directory_manager import DirectoryManager
from carlogger.items.car import Car
from carlogger.items.car_info import CarInfo
from carlogger.cli.arg_executor import ArgExecutor, AddArgExecutor, ReadArgExecutor, DeleteArgExecutor, \
    UpdateArgExecutor, ExportArgExecutor, ImportArgExecutor
from carlogger.items.component_collection import ComponentCollection
from carlogger.items.car_component import CarComponent
from carlogger.items.log_entry import ScheduledLogEntry
from carlogger.rename_agent import RenameAgent
from carlogger.util import check_file_extension_validity, is_scheduled_entry


class AppSession:
    """Setup current app session, load saved info: load collections, components and log entries."""
    def __init__(self, directory_manager: DirectoryManager):
        self.directory_manager = directory_manager
        self.arg_executor: ArgExecutor = ...
        self.gui = None

        self.cars: list[Car] = []
        self.selected_car: Car = ...

    def create_gui(self, gui: RootWindow):
        self.gui = gui
        self.gui.app_session = self

        self.cars = self.directory_manager.load_all_car_dir()

        self.gui.cars = self.cars
        self.selected_car = self.cars[0]

        self.gui.start_mainloop()

    def request_item_update(self):
        self.reload_cars()
        self.gui.cars = self.cars

    def reload_cars(self):
        for car in self.cars:
            self.save_car(car.car_info.name)

        self.cars = self.directory_manager.load_all_car_dir()

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
            case 'import':
                self.arg_executor = ImportArgExecutor(parsed_args, self, raw_args)
            case 'export':
                self.arg_executor = ExportArgExecutor(parsed_args, self, raw_args)
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
            self.delete_collection_children(car_name, coll)

        self.directory_manager.remove_item(coll)
        car.delete_collection(collection_name)
        self.directory_manager.update_car_directory(car)

    def delete_collection_children(self, car_name: str, collection: ComponentCollection):
        for ch in collection.children:
            if type(ch) == ComponentCollection:
                self.delete_collection(car_name, ch.name)
            else:
                self.delete_component(car_name, collection.name, ch.name)

    def delete_component_children(self, component: CarComponent, car: Car):
        component.delete_children(self)
        self.directory_manager.update_car_directory(car)

    def delete_car_children(self, car: Car):
        for ch in car.collections:
            if len(ch.children) > 0:
                self.delete_collection_children(car.car_info.name, ch)
            self.delete_collection(car.car_info.name, ch.name)

    def add_new_component(self, car_name: str, collection_name: str, component_name: str):
        """Add new collection to specified car and update save directory."""
        car = self.get_car_by_name(car_name)
        collection = car.get_collection_by_name(collection_name)
        new_comp = collection.create_component(component_name)
        new_comp.parent = collection
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

    def delete_entry_by_id(self, car_name: str, entry_id: str, component: CarComponent = None):
        """Delete entry via their unique ID."""
        car = self.get_car_by_name(car_name)

        if not component:
            component = car.get_component_of_entry_by_entry_id(entry_id)

        component.delete_entry_by_id(entry_id)
        self.directory_manager.update_car_directory(car)

    def delete_entries_by_id(self, car_name: str, entry_ids: list[str], component: CarComponent = None):
        """Delete batch of entries from component via their unique ID."""
        car = self.get_car_by_name(car_name)

        if not component:
            component = car.get_component_of_entry_by_entry_id(entry_ids[0])

        for entry_id in entry_ids:
            component.delete_entry_by_id(entry_id)

        self.directory_manager.update_car_directory(car)

    def update_car_info(self, car: Car, updated_data: dict[str, ...]):
        """Update target car info values and update the save file."""

        legacy_car_info_path = car.car_info.path

        for key, value in updated_data.items():
            setattr(car.car_info, key, value)

        # Create new directory and copy items over when changing name of the car
        if 'name' in updated_data.keys():
            car.name = updated_data['name']
            self.directory_manager.rename_car_dir(car, legacy_car_info_path)
        else:
            self.directory_manager.update_car_directory(car)

    def update_component_or_collection(self, parent_car: Car, item, updated_data: dict[str, ...]):
        self.directory_manager.remove_item(item)

        item = self._reparent_item(updated_data, item) or item

        if 'name' in updated_data.keys():
            r = RenameAgent(item, updated_data['name'], self.directory_manager.data_manager)

        for key, value in updated_data.items():
            setattr(item, key, value)

        self.directory_manager.update_car_directory(parent_car)

    def _reparent_item(self, data: dict, item_ref):
        if 'parent' in data.keys():
            match item_ref.__class__.__name__:
                case 'ComponentCollection':
                    new_parent = data.get('parent')

                    new_parent.collections.append(item_ref)
                    item_ref.parent.collections.remove(item_ref)
                    item_ref.parent = new_parent
                    item_ref.path = Path(new_parent.path).joinpath('collections')

                    self._reparent_child_elements(item_ref)

                    data.pop('parent')

                case _:
                    new_parent = data.get('parent')

                    item_ref.parent.components.remove(item_ref)
                    new_parent.components.append(item_ref)
                    item_ref.parent = new_parent
                    item_ref.path = Path(new_parent.path).parent.joinpath('components')

                    data.pop('parent')

                    if car := data.get('car'):
                        self.directory_manager.data_manager.save_file(item_ref)
                        self.directory_manager.update_car_directory(car)
                        data.pop('car')

                    return item_ref

    def _reparent_child_elements(self, item_ref):
        to_del = []
        for comp in item_ref.components:
            to_del.append(comp.get_target_path(self.directory_manager.data_manager.suffix))
            self._reparent_item({'parent': item_ref}, comp)

        for coll in item_ref.collections:
            to_del.append(coll.get_target_path(self.directory_manager.data_manager.suffix))
            self._reparent_item({'parent': item_ref.car}, coll)

        for pa in to_del:
            os.remove(pa)

        self.directory_manager.update_car_directory(item_ref.car)

        return item_ref

    def update_entry(self, parent_car: Car, entry, updated_data: dict[str, ...]):
        """Update values of target entry and update the save file."""
        for key, value in updated_data.items():
            setattr(entry, key, value)

        if is_scheduled_entry(entry):
            entry.get_new_date()

        if entry.component.car_mileage_needs_update(entry):
            self.update_car_info(parent_car, {'mileage': entry.mileage})

        path = entry.component.get_target_path(self.directory_manager.data_manager.suffix)
        self.directory_manager.data_manager.save_file(entry.component, path)

    def set_scheduled_entry_as_done(self, parent_car: Car, entry: ScheduledLogEntry):
        """Update values of target entry and update the save file."""
        repeated_entry = entry.component.mark_scheduled_entry_as_done(entry.id)
        path = entry.component.get_target_path(self.directory_manager.data_manager.suffix)
        self.directory_manager.data_manager.save_file(entry.component, path)
        return repeated_entry

    def export_item_to_file(self, item, path, *values):
        check_file_extension_validity(path)
        self.directory_manager.match_extension_to_filedata_manager(path).save_file(item, path, *values)

    def import_item_from_file(self, item_class_name: str, path, no_children=False, **parents):
        check_file_extension_validity(path)

        match item_class_name:
            case 'car':
                data = self.directory_manager.data_manager.load_file(path)
                new_car = self.add_new_car(data)

                if not no_children and data.get('collections'):
                    for coll in data['collections']:
                        new_car.create_collection(coll)

                self.directory_manager.update_car_directory(new_car)
            case 'collection':
                car_name = parents.get('car')
                car = self.get_car_by_name(car_name)
                data = self.directory_manager.data_manager.load_file(path)
                self._collection_from_file(data, car, no_children=no_children)
                self.directory_manager.update_car_directory(car)
            case 'component':
                data = self.directory_manager.data_manager.load_file(path)
                car_name = parents.get('car')
                collection_name = parents.get('collection')

                car = self.get_car_by_name(car_name)
                collection = car.get_collection_by_name(collection_name)
                new_comp = collection.create_component(data['name'])

                if not new_comp:
                    return

                if not no_children:
                    for entry in data['log_entries']:
                        new_comp.create_entry(entry)

                    for entry in data['scheduled_log_entries']:
                        new_comp.create_scheduled_entry(entry)

                self.directory_manager.update_car_directory(car)

    def _collection_from_file(self, data: dict, car: Car, no_children=False):
        car.create_collection(data['name'])
        self.directory_manager.update_car_directory(car)
        collection = car.get_collection_by_name(data['name'])

        for k in data.keys():
            setattr(collection, k, data.get(k))

        if not no_children:
            comps = []
            for comp in data['components']:
                new_comp = CarComponent(**comp)
                comps.append(new_comp)
            setattr(collection, 'components', comps)
        else:
            setattr(collection, 'collections', [])
            setattr(collection, 'components', [])

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
