"""Executes parsed CLI arguments"""

import uuid

from abc import abstractmethod, ABC

from carlogger.car import Car
from carlogger.component_collection import ComponentCollection
from carlogger.car_component import CarComponent
from carlogger.log_entry import LogEntry
from carlogger.entry_category import EntryCategory
from carlogger.session import AppSession
from carlogger.util import is_date


class ArgExecutor(ABC):
    """Abstract ReadArgExecutor class for executing functions related to console args."""
    @abstractmethod
    def evaluate_args(self):
        """Execute mapped functions based on passed args."""
        return


class ReadArgExecutor(ArgExecutor):
    """Contains mapped dictionary of functions to execute on program start based on passed console arguments."""
    def __init__(self, parsed_args: dict, app_session: AppSession):
        self.app = app_session
        self.args = parsed_args
        self.arg_func_map = {'car': self.load_car_dir,
                             'collection': self.get_collections,
                             'component': self.get_components,
                             'entry': self.get_entries}

        self.cached_car: Car = ...
        self.cached_coll: list[ComponentCollection] = ...
        self.cached_comp: list[CarComponent] = ...
        self.cached_entries: list[LogEntry] = ...

        self.verbosity_map = {"car": self.print_car_info,
                              "collection": self.print_collections,
                              "component": self.print_components,
                              "entry": self.print_entries}

    def evaluate_args(self):
        """Evaluate args list property by calling the matching functions."""
        executed_args = []

        args = list(filter(self._filter_empty_keys, self.args.keys()))

        try:
            for arg in args:
                self.arg_func_map.get(arg)()
                executed_args.append(arg)
        except KeyError:
            print(f"Invalid console argument:")
            raise SystemExit(1)

        self.print_info_based_on_verbosity(executed_args)

    def print_info_based_on_verbosity(self, executed_args: list[str]):
        """Print console output based on passed args. Only the highest priority argument result will be printed out.\n
        Priority: Entries -> Components -> Collections -> Car Info\n
        'executed_args' is simply a list of correctly executed args, last item being chosen for evaluation"""
        self.verbosity_map.get(executed_args[-1])()

    def load_car_dir(self):
        """Load and cache car directory for the current session."""
        if car := self.args.get('car'):
            loaded_car = self.app.directory_manager.load_car_dir(car)
            self.app.cars.append(loaded_car)
            self.cached_car = loaded_car

    def print_car_info(self):
        """Print car info of the loaded/cached car."""
        print(self.cached_car.get_formatted_info())

    def get_collections(self) -> list[ComponentCollection] | None:
        """Return list of component collections of cached car."""
        collections: list[str] = self.args.get('collection')
        loaded_collections: list[ComponentCollection] = []

        if not collections:
            return

        if not self.cached_car:
            return

        for collection in collections:
            new_coll = self.cached_car.get_collection_by_name(collection)

            if new_coll:
                loaded_collections.append(new_coll)

        self.cached_coll = loaded_collections
        self._get_element_diff('Component collection', collections, loaded_collections)

        return loaded_collections

    def print_collections(self):
        """Print desired collections."""
        for coll in self.cached_coll:
            print(coll.get_formatted_info())

    def get_components(self) -> list[CarComponent] | None:
        """Return list of components of cached car."""
        components: list[str] = self.args.get('component')
        loaded_comp: list[CarComponent] = []

        if not components:
            return

        if self.cached_car:
            for comp in components:
                new_comp = self.cached_car.get_component_by_name(comp)

                if new_comp:
                    loaded_comp.append(new_comp)
        elif self.cached_coll:
            for comp in components:
                for coll in self.cached_coll:
                    new_comp = coll.get_component_by_name(comp)

                    if new_comp:
                        loaded_comp.append(new_comp)
        else:
            return

        self.cached_comp = loaded_comp
        self._get_element_diff('Car component', components, loaded_comp)

        return loaded_comp
    
    def print_components(self):
        """Print desired components from cached car."""
        for comp in self.cached_comp:
            print(comp.get_formatted_info())

    def get_entries(self) -> list[LogEntry] | None:
        """Return list of log entries of cached car."""
        entries: list[str] = list(set(self.args.get('entry')))
        loaded_entries: list[LogEntry] = []
        filter_keys = [self.get_entry_filter_key(key) for key in entries]

        if not entries:
            return

        if self.cached_car:
            all_car_entries = self.cached_car.get_all_entry_logs()

            for entry in all_car_entries:
                for key in filter_keys:
                    if entry.to_json().get(key) in entries:
                        loaded_entries.append(entry)
        elif self.cached_coll:
            # Get all entry logs in all cached collections and filter through
            all_coll_entries = [coll.get_all_log_entries(coll.children) for coll in self.cached_coll]
            all_entries = []
            [all_entries.extend(entry_list) for entry_list in all_coll_entries]

            for entry in all_entries:
                for key in filter_keys:
                    if entry.to_json().get(key) in entries:
                        loaded_entries.append(entry)
        elif self.cached_comp:
            # Get all entry logs in all cached components and filter through
            all_comp_entries = [comp.log_entries for comp in self.cached_comp]
            all_entries = []
            [all_entries.extend(entry_list) for entry_list in all_comp_entries]

            for entry in all_entries:
                for key in filter_keys:
                    if entry.to_json().get(key) in entries:
                        loaded_entries.append(entry)

        loaded_entries = list(set(loaded_entries))
        self.cached_entries = loaded_entries

        return loaded_entries

    def print_entries(self):
        """Print desired entries."""
        for entry in self.cached_entries:
            print(entry.get_formatted_info())

    def get_entry_filter_key(self, passed_arg: str) -> str:
        """Get type of filter for entries based on passed arg."""
        if type(passed_arg) == uuid.UUID:
            return 'id'

        if is_date(passed_arg):
            return 'date'

        if passed_arg in [member for member in EntryCategory]:
            return 'category'

        return 'desc'

    def _filter_empty_keys(self, key: str) -> bool:
        return self.args.get(key) is not None

    def _get_element_diff(self, class_name: str, expected: list[str], results: list):
        names = [elem.name for elem in results]

        for name in expected:
            if name not in names:
                print(f"WARNING: {class_name} '{name}' was not found!")
