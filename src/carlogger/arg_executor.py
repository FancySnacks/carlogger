"""Executes parsed CLI arguments"""


from carlogger.car import Car
from carlogger.component_collection import ComponentCollection
from carlogger.car_component import CarComponent
from carlogger.session import AppSession


class ArgExecutor:
    """Contains mapped dictionary of functions to execute on program start based on passed console arguments."""
    def __init__(self, parsed_args: dict, app_session: AppSession):
        self.app = app_session
        self.args = parsed_args
        self.arg_func_map = {'car': self.load_car_dir,
                             'collection': self.print_collections,
                             'component': self.print_components}

        self.cached_car: Car = ...
        self.cached_coll: list[ComponentCollection] = ...
        self.cached_comp: list[CarComponent] = ...

    def evaluate_args(self):
        args = list(filter(self._filter_empty_keys, self.args.keys()))

        try:
            for arg in args:
                self.arg_func_map.get(arg)()
        except KeyError:
            print(f"Invalid console argument:")
            raise SystemExit(1)

    def load_car_dir(self):
        if car := self.args.get('car'):
            loaded_car = self.app.directory_manager.load_car_dir(car)
            self.app.cars.append(loaded_car)

            self.cached_car = loaded_car
            #print(loaded_car)

    def get_collections(self):
        collections: list[str] = self.args.get('collection')
        loaded_collections = []

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
        collections = self.get_collections()

        for coll in collections:
            print(coll)

    def get_components(self):
        components = self.args.get('component')
        loaded_comp = []

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
        components = self.get_components()

        for comp in components:
            print(comp)

    def _filter_empty_keys(self, key: str) -> bool:
        return self.args.get(key) is not None

    def _get_element_diff(self, class_name: str, expected: list[str], results: list):
        names = [elem.name for elem in results]

        for name in expected:
            if name not in names:
                print(f"WARNING: {class_name} '{name}' was not found!")
