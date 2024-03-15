"""Executes parsed CLI arguments"""

from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from carlogger.session import AppSession

from carlogger.car import Car
from carlogger.component_collection import ComponentCollection
from carlogger.car_component import CarComponent
from carlogger.log_entry import LogEntry
from carlogger.entryfilter import EntryFilter


class ArgExecutor(ABC):
    """Abstract ReadArgExecutor class for executing functions related to console args."""
    @abstractmethod
    def __init__(self, parsed_args: dict, app_session: AppSession):
        return

    @abstractmethod
    def evaluate_args(self):
        """Execute mapped functions based on passed args."""
        return


class AddArgExecutor(ArgExecutor):
    """Handles 'add' subparser for adding new cars, collections and entry logs."""
    def __init__(self, parsed_args: dict, app_session: AppSession):
        self.parsed_args = parsed_args
        self.app_session = app_session

    def evaluate_args(self):
        """Execute mapped functions based on passed args."""
        # remove args that are not related to this executor and subparser
        vals = {key: value for (key, value) in self.parsed_args.items() if self.parsed_args.get(key)}
        self.app_session.add_new_car(vals)


class ReadArgExecutor(ArgExecutor):
    """Handles 'read' subparser for printing out car info, collections and entries into console."""
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
                if func := self.arg_func_map.get(arg):
                    func()
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

        entry_filter = EntryFilter()

        entries = self._clamp_cli_entries(entries)

        if self.cached_car:
            all_car_entries = self.cached_car.get_all_entry_logs()
            filtered_entries = entry_filter.apply_filters_to_entry_list(entries, all_car_entries)
            print(entry_filter.filters)

            for entry in filtered_entries:
                loaded_entries.append(entry)

        elif self.cached_coll:
            # Get all entry logs in all cached collections and filter through
            all_coll_entries = [coll.get_all_log_entries(coll.children) for coll in self.cached_coll]
            all_entries = []
            [all_entries.extend(entry_list) for entry_list in all_coll_entries]

            filtered_entries = entry_filter.apply_filters_to_entry_list(entries, all_entries)

            for entry in filtered_entries:
                loaded_entries.append(entry)

        elif self.cached_comp:
            # Get all entry logs in all cached components and filter through
            all_comp_entries = [comp.log_entries for comp in self.cached_comp]
            all_entries = []
            [all_entries.extend(entry_list) for entry_list in all_comp_entries]

            filtered_entries = entry_filter.apply_filters_to_entry_list(entries, all_entries)

            for entry in filtered_entries:
                loaded_entries.append(entry)

        loaded_entries = list(set(loaded_entries))
        self.cached_entries = loaded_entries

        return loaded_entries

    def print_entries(self):
        """Print desired entries."""
        for entry in self.cached_entries:
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

    def _filter_empty_keys(self, key: str) -> bool:
        return self.args.get(key) is not None

    def _get_element_diff(self, class_name: str, expected: list[str], results: list):
        names = [elem.name for elem in results]

        for name in expected:
            if name not in names:
                print(f"WARNING: {class_name} '{name}' was not found!")
