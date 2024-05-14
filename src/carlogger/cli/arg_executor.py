"""Executes parsed CLI arguments"""

from __future__ import annotations

import dataclasses

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from carlogger.session import AppSession

from carlogger.items.car import Car
from carlogger.items.car_info import CarInfo
from carlogger.items.component_collection import ComponentCollection
from carlogger.items.car_component import CarComponent
from carlogger.items.log_entry import LogEntry
from carlogger.items.entryfilter import EntryFilter
from carlogger.items.item_sorter import ItemSorter
from carlogger.util import is_valid_entry_id, sort_key_is_attrib


class ArgExecutor(ABC):
    """Abstract ReadArgExecutor class for executing functions related to console args."""
    @abstractmethod
    def __init__(self, parsed_args: dict, app_session: AppSession, raw_args: list[str]):
        return

    @abstractmethod
    def evaluate_args(self):
        """Execute mapped functions based on passed args."""
        return


class DeleteArgExecutor(ArgExecutor):
    """Handles 'delete' subparser for deleting cars, collections or entry logs."""
    def __init__(self, parsed_args: dict, app_session: AppSession, raw_args: list[str]):
        self.parsed_args = parsed_args
        self.app_session = app_session
        self.raw_args = raw_args[1::]

        self.arg_func_map = {'car': self.delete_car,
                             'collection': self.delete_collection,
                             'component': self.delete_component,
                             'entry': self.delete_entry}

    def evaluate_args(self):
        """Execute mapped functions based on passed args."""
        context = self._recognize_context()
        self.arg_func_map.get(context)()

    def delete_car(self):
        car_name = self.parsed_args['name']

        if self.parsed_args.get('clear'):
            car = self.app_session.get_car_by_name(car_name)
            self.app_session.delete_car_children(car)
        elif any([self._check_if_car_is_empty(car_name),
                self.parsed_args.get('forced')]):
            self.app_session.delete_car(car_name)
        else:
            print(f"ERROR: '{car_name}' cannot be removed because it's not empty!")

    def delete_collection(self):
        car_name = self.parsed_args['car']
        collection_name = self.parsed_args['name']

        if self.parsed_args.get('clear'):
            car = self.app_session.get_car_by_name(car_name)
            coll_to_clear = car.get_collection_by_name(collection_name)
            self.app_session.delete_collection_children(car_name, coll_to_clear)
        elif any([self._check_if_collection_is_empty(collection_name, car_name),
            self.parsed_args.get('forced')]):
            self.app_session.delete_collection(car_name, collection_name)
        else:
            print(f"ERROR: '{collection_name}' cannot be removed because it's not empty!")

    def delete_component(self):
        car_name = self.parsed_args['car']
        collection_name = self.parsed_args['collection']
        component_name = self.parsed_args['name']

        if self.parsed_args.get('clear'):
            car = self.app_session.get_car_by_name(car_name)
            comp_to_clear = car.get_component_by_name(component_name)
            self.app_session.delete_component_children(comp_to_clear, car)
        elif any([self._check_if_component_is_empty(component_name, car_name),
            self.parsed_args.get('forced')]):
            self.app_session.delete_component(car_name, collection_name, component_name)
        else:
            print(f"ERROR: '{component_name}' cannot be removed because it's not empty!")

    def delete_entry(self):
        car_name = self.parsed_args['car']
        entry = self.parsed_args['id']

        match self._get_entry_delete_method(entry):
            case 'index':
                component_name = self.parsed_args.get('component')

                if not component_name:
                    print(f"ERROR: Could not delete entry of index '{entry}' because you have not specified which "
                          f"component it belongs to")
                    return

                self.app_session.delete_entry_by_index(car_name, component_name, int(entry))

            case 'id':
                self.app_session.delete_entry_by_id(car_name, entry)

    def _get_entry_delete_method(self, entry_arg: str) -> str:
        if entry_arg.isdigit():
            return 'index'

        if is_valid_entry_id(entry_arg):
            return 'id'

    def _recognize_context(self):
        """See which item user wants to delete."""
        if len(self.raw_args) < 2:
            raise ValueError(
                "Item to delete was not specified. (use one of these: 'car', 'collection', 'component', 'entry')")

        match self.raw_args[1]:
            case 'car': return 'car'
            case 'collection': return 'collection'
            case 'component': return 'component'
            case 'entry': return 'entry'

    def _check_if_car_is_empty(self, car_name: str) -> bool:
        car = self.app_session.get_car_by_name(car_name)
        return len(car.collections) < 1

    def _check_if_collection_is_empty(self, collection_name: str, car_name: str) -> bool:
        coll = self.app_session.get_car_by_name(car_name).get_collection_by_name(collection_name)
        return len(coll.children) < 1

    def _check_if_component_is_empty(self, component_name: str, car_name: str) -> bool:
        comp = self.app_session.get_car_by_name(car_name).get_component_by_name(component_name)
        return len(comp.log_entries) < 1


class AddArgExecutor(ArgExecutor):
    """Handles 'add' subparser for adding new cars, collections and entry logs."""
    def __init__(self, parsed_args: dict, app_session: AppSession, raw_args: list[str]):
        self.parsed_args = parsed_args
        self.app_session = app_session
        self.raw_args = raw_args[1::]

        self.arg_func_map = {'car': self.add_new_car,
                             'collection': self.add_new_collection,
                             'component': self.add_new_component,
                             'entry': self.add_new_entry,
                             'scheduled_entry': self.add_new_scheduled_entry}

    def evaluate_args(self):
        """Execute mapped functions based on passed args."""
        context = self._recognize_context()
        self.arg_func_map.get(context)()

    def add_new_car(self):
        """Create a new car directory based on passed argument values."""
        valid_car_keys = [field.name for field in dataclasses.fields(CarInfo)]
        vals = {key: value for (key, value) in self.parsed_args.items() if key in valid_car_keys}
        self.app_session.add_new_car(vals)

    def add_new_collection(self):
        """Create a new car collection belonging to specified car."""
        car_name = self.parsed_args['car']
        coll_name = self.parsed_args['name']

        if parent_coll := self.parsed_args.get('parent'):
            self.app_session.add_new_nested_collection(car_name, coll_name, parent_coll)
        else:
            self.app_session.add_new_collection(car_name, coll_name)

    def add_new_component(self):
        """Create a new car component belonging to a specified collection and car."""
        car_name = self.parsed_args['car']
        coll_name = self.parsed_args['collection']
        comp_name = self.parsed_args['name']
        self.app_session.add_new_component(car_name, coll_name, comp_name)

    def add_new_entry(self):
        """Create a new log entry belonging to a specified car and component."""
        car_name = self.parsed_args['car']
        coll_name = self.parsed_args['collection']
        comp_name = self.parsed_args['component']

        valid_entry_keys = [field.name for field in dataclasses.fields(LogEntry)]
        entry_data = {key: value for (key, value) in self.parsed_args.items() if key in valid_entry_keys}

        self.app_session.add_new_entry(car_name, coll_name, comp_name, entry_data)

    def add_new_scheduled_entry(self):
        """Create a new car component belonging to a specified car, collection and component."""
        car_name = self.parsed_args['car']
        coll_name = self.parsed_args['collection']
        comp_name = self.parsed_args['component']

        entry_data = {key: value for (key, value) in self.parsed_args.items()}

        self.app_session.add_new_scheduled_entry(car_name, coll_name, comp_name, entry_data)

    def _recognize_context(self) -> str:
        """What do we wish to create; car, collection, component or log entry?"""

        if len(self.raw_args) < 2:
            raise ValueError(
                "Item to add was not specified. (use one of these: 'car', 'collection', 'component', 'entry')")

        return self.raw_args[1]


class ReadArgExecutor(ArgExecutor):
    """Handles 'read' subparser for printing out car info, collections and entries into console."""
    def __init__(self, parsed_args: dict, app_session: AppSession, raw_args: list[str]):
        self.app = app_session
        self.args = parsed_args
        self.raw_args = raw_args[1::]

        self.arg_func_map = {'car': self.get_car,
                             'collection': self.get_collection,
                             'component': self.get_component,
                             'entry': self.get_entries}

    def evaluate_args(self):
        """Evaluate args list property by calling the matching functions."""
        context = self._recognize_context()
        self.arg_func_map.get(context)()

    def _recognize_context(self) -> str:
        """What do we wish to read; car, collection, component or log entry?"""

        if len(self.raw_args) < 2:
            raise ValueError(
                "Item to read was not specified. (use one of these: 'car', 'collection', 'component', 'entry')")

        match self.raw_args[1]:
            case 'car': return 'car'
            case 'collection': return 'collection'
            case 'component': return 'component'
            case 'entry': return 'entry'

    def get_car(self):
        """Find car by name and return car info."""
        car_name = self.args.get('name')

        if car_name == '*':
            sort_key = self.args.get('sort')
            reverse_sort = self.args.get('reverse')
            all_cars = self.app.directory_manager.load_all_car_dir()
            all_car_infos = [c.car_info for c in all_cars]

            if sort_key:
                if sort_key_is_attrib(sort_key, all_cars[0]):
                    item_sorter = ItemSorter(items=all_car_infos, sort_method=sort_key)
                    all_car_infos = item_sorter.get_sorted_list(reverse_order=reverse_sort)
                    print([car.name for car in all_car_infos])
                else:
                    print([c.name for c in all_car_infos])
        else:
            car = self.app.get_car_by_name(car_name)
            self.print_car_info(car)

    def print_car_info(self, car: Car):
        """Print car info of the loaded/cached car."""
        print(car.get_formatted_info())
        print(*car.collections)

    def get_collection(self):
        """Return list of component collections of target car."""
        car_name = self.args.get('car')
        collection_name = self.args.get('name')
        car = self.app.get_car_by_name(car_name)

        # Print ALL collections
        if collection_name == '*':
            sort_key = self.args.get('sort')
            reverse_sort = self.args.get('reverse')
            all_collections = car.collections

            if sort_key:
                if sort_key_is_attrib(sort_key, all_collections[0]):
                    item_sorter = ItemSorter(items=all_collections, sort_method=sort_key)
                    all_collections = item_sorter.get_sorted_list(reverse_order=reverse_sort)
                else:
                    item_sorter = ItemSorter(items=all_collections, sort_method=sort_key)
                    all_collections = item_sorter.get_sorted_list(reverse_order=reverse_sort)

            print(*all_collections)

        # Print single collection via name
        else:
            collection = car.get_collection_by_name(collection_name)
            self.print_collection(collection)

    def print_collection(self, collection: ComponentCollection):
        """Print desired collections."""
        print(collection.get_formatted_info())

    def get_component(self):
        """Return list of components of target car."""
        car_name = self.args.get('car')
        component_name = self.args.get('name')
        car = self.app.get_car_by_name(car_name)

        if component_name == '*':
            sort_key = self.args.get('sort')
            reverse_sort = self.args.get('reverse')
            components = [c.components for c in car.collections]
            all_components = []
            [all_components.extend(clist) for clist in components]

            if sort_key:
                if sort_key_is_attrib(sort_key, all_components[0]):
                    item_sorter = ItemSorter(items=all_components, sort_method=sort_key)
                    all_components = item_sorter.get_sorted_list(reverse_order=reverse_sort)
                else:
                    item_sorter = ItemSorter(items=all_components, sort_method=sort_key)
                    all_components = item_sorter.get_sorted_list(reverse_order=reverse_sort)

            print(*all_components)
        else:
            component = car.get_component_by_name(component_name)
            self.print_component(component)
    
    def print_component(self, component: CarComponent):
        """Print desired components from cached car."""
        print(component.get_formatted_info())

    def get_entries(self):
        """Return list of log entries of cached car."""
        entries = self.args.get('data') or []
        entries: list[str] = list(set(entries))

        loaded_entries: list[LogEntry] = []

        car_name = self.args.get('car')
        car = self.app.get_car_by_name(car_name)

        entry_filter = EntryFilter()
        entries = self._clamp_cli_entries(entries)

        all_car_entries = car.get_all_entry_logs()
        filtered_entries = entry_filter.apply_filters_to_entry_list(entries, all_car_entries)
        #print(entry_filter.filters)

        for entry in filtered_entries:
            loaded_entries.append(entry)

        loaded_entries = list(set(loaded_entries))

        sort_key = self.args.get('sort')
        reverse_sort = self.args.get('reverse')
        if sort_key:
            if sort_key_is_attrib(sort_key, loaded_entries[0]):
                item_sorter = ItemSorter(items=loaded_entries, sort_method=sort_key)
                loaded_entries = item_sorter.get_sorted_list(reverse_order=reverse_sort)
            else:
                item_sorter = ItemSorter(items=loaded_entries, sort_method=sort_key)
                loaded_entries = item_sorter.get_sorted_list(reverse_order=reverse_sort)

        self.print_entries(loaded_entries)

    def print_entries(self, entries: list[LogEntry]):
        """Print desired entries."""
        for entry in entries:
            print(entry.get_formatted_info())

    def _clamp_cli_entries(self, entries: list[str]) -> list[str]:
        if not entries:
            entries.append('*')
            return entries

        if len(entries) == 1:
            match = EntryFilter.count_flag_exists_in_arg_list(entries)
            if len(match) > 0:
                return ['*', match[0]]

        return entries


class UpdateArgExecutor(ArgExecutor):
    """Handles 'update' subparser for updating car, collection, component or entry log data."""
    def __init__(self, parsed_args: dict, app_session: AppSession, raw_args: list[str]):
        self.parsed_args = parsed_args
        self.app_session = app_session
        self.raw_args = raw_args[1::]

        self.arg_func_map = {'car': self.update_car,
                             'collection': self.update_collection,
                             'component': self.update_component,
                             'entry': self.update_entry}

    def evaluate_args(self):
        """Execute mapped functions based on passed args."""
        context = self._recognize_context()
        self.arg_func_map.get(context)()

    def update_car(self):
        """Update car data based on passed arguments."""
        car_name = self.parsed_args['car']
        car = self.app_session.get_car_by_name(car_name)

        entry_data = self._clamp_updated_values(car.car_info)
        self.app_session.update_car_info(car, entry_data)

    def update_collection(self):
        """Update collection data based on passed arguments."""
        car_name = self.parsed_args['car']
        coll_name = self.parsed_args['collection']
        car = self.app_session.get_car_by_name(car_name)
        collection = car.get_collection_by_name(coll_name)

        new_coll_data = self._clamp_updated_values(collection)
        self.app_session.update_component_or_collection(car, collection, new_coll_data)

    def update_component(self):
        """Update component data based on passed arguments."""
        car_name = self.parsed_args['car']
        comp_name = self.parsed_args['component']
        car = self.app_session.get_car_by_name(car_name)
        component = car.get_component_by_name(comp_name)

        new_comp_data = self._clamp_updated_values(component)
        self.app_session.update_component_or_collection(car, component, new_comp_data)

    def update_entry(self):
        """Update entry data based on passed arguments."""
        car_name = self.parsed_args['car']
        entry_id = self.parsed_args['id']
        car = self.app_session.get_car_by_name(car_name)
        entry = car.get_entry_by_id(entry_id)

        new_entry_data = self._clamp_updated_values(entry)
        self.app_session.update_entry(car, entry, new_entry_data)

    def _clamp_updated_values(self, item: CarInfo | ComponentCollection | CarComponent | LogEntry) -> dict:
        """Filter out data that is empty, not set or exactly the same as existing one in target item."""
        new_data = self._get_used_keys(item)
        clamped_dict = {}

        for key in new_data.keys():
            data = new_data.get(key)
            if data:
                if data != getattr(item, key, new_data[key]):
                    clamped_dict[key] = new_data[key]

        return clamped_dict

    def _get_used_keys(self, item: CarInfo | CarComponent | ComponentCollection | LogEntry) -> dict[str, ...]:
        """Return properties used by the object."""
        valid_keys = [field.name for field in dataclasses.fields(item.__class__)]
        updated_data = {key: value for (key, value) in self.parsed_args.items() if key in valid_keys}
        return updated_data

    def _recognize_context(self) -> str:
        """Which item to update; car, collection, component or log entry?"""

        if len(self.raw_args) < 2:
            raise ValueError(
                "Item to update was not specified. (use one of these: 'car', 'collection', 'component', 'entry')")

        match self.raw_args[1]:
            case 'car': return 'car'
            case 'collection': return 'collection'
            case 'component': return 'component'
            case 'entry': return 'entry'


class ExportArgExecutor(ArgExecutor):
    """Handles 'export' subparser for exporting item into a file."""
    def __init__(self, parsed_args: dict, app_session: AppSession, raw_args: list[str]):
        self.parsed_args = parsed_args
        self.app_session = app_session
        self.raw_args = raw_args[1::]

        self.arg_func_map = {'car': self.export_car,
                             'collection': self.export_collection,
                             'component': self.export_component}

    def evaluate_args(self):
        """Execute mapped functions based on passed args."""
        context = self._recognize_context()
        self.arg_func_map.get(context)()

    def export_car(self):
        save_path = self.parsed_args['path']
        car_name = self.parsed_args['name']
        car = self.app_session.get_car_by_name(car_name)
        self.app_session.export_item_to_file(car.car_info, save_path)

    def export_collection(self):
        save_path = self.parsed_args['path']
        coll_name = self.parsed_args['name']
        car_name = self.parsed_args['car']

        car = self.app_session.get_car_by_name(car_name)
        collection = car.get_collection_by_name(coll_name)

        self.app_session.export_item_to_file(collection, save_path)

    def export_component(self):
        save_path = self.parsed_args['path']
        comp_name = self.parsed_args['name']
        coll_name = self.parsed_args['collection']
        car_name = self.parsed_args['car']

        car = self.app_session.get_car_by_name(car_name)
        collection = car.get_collection_by_name(coll_name)
        component = collection.get_component_by_name(comp_name)

        self.app_session.export_item_to_file(component, save_path)

    def _recognize_context(self) -> str:
        """Which item to export; car, collection or component?"""
        match self.raw_args[1]:
            case 'car': return 'car'
            case 'collection': return 'collection'
            case 'component': return 'component'


class ImportArgExecutor(ArgExecutor):
    """Handles 'import' subparser for importing item into a file."""
    def __init__(self, parsed_args: dict, app_session: AppSession, raw_args: list[str]):
        self.parsed_args = parsed_args
        self.app_session = app_session
        self.raw_args = raw_args[1::]

        self.arg_func_map = {'car': self.import_car,
                             'collection': self.import_collection,
                             'component': self.import_component}

    def evaluate_args(self):
        """Execute mapped functions based on passed args."""
        context = self._recognize_context()
        self.arg_func_map.get(context)()

    def import_car(self):
        load_path = self.parsed_args['path']
        self.app_session.import_item_from_file('car', load_path)

    def import_collection(self):
        load_path = self.parsed_args['path']
        car_name = self.parsed_args['car']

        self.app_session.import_item_from_file('collection', load_path, car=car_name)

    def import_component(self):
        load_path = self.parsed_args['path']
        coll_name = self.parsed_args['collection']
        car_name = self.parsed_args['car']

        self.app_session.import_item_from_file('component', load_path, car=car_name, collection=coll_name)

    def _recognize_context(self) -> str:
        """Which item to import; car, collection or component?"""
        match self.raw_args[1]:
            case 'car': return 'car'
            case 'collection': return 'collection'
            case 'component': return 'component'
