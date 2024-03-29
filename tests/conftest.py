import pytest
import pathlib

from carlogger.items.car import Car
from carlogger.items.car_component import CarComponent
from carlogger.items.car_info import CarInfo
from carlogger.items.component_collection import ComponentCollection
from carlogger.items.entry_category import EntryCategory
from carlogger.directory_manager import DirectoryManager
from carlogger.filedata_manager import JSONFiledataManager


with open(pathlib.Path.cwd().joinpath("tests/add_arg_test"), "r") as f:
    commands = [c.replace("\n", "").replace('"', "").split() for c in f.readlines()]
    keys = ['car', 'collection', 'component', 'entry']
    args = list(zip(keys, commands))

ADD_ARGS = {k: v for k, v in args}

with open(pathlib.Path.cwd().joinpath("tests/delete_arg_test"), "r") as f:
    commands = [c.replace("\n", "").replace('"', "").split() for c in f.readlines()]
    keys = ['entry', 'component', 'collection', 'car']
    args = list(zip(keys, commands))

DEL_ARGS = {k: v for k, v in args}


@pytest.fixture
def add_cmd() -> dict:
    return ADD_ARGS


@pytest.fixture
def delete_cmd() -> dict:
    return DEL_ARGS


@pytest.fixture(scope="session")
def mock_car_info() -> dict:
    d = {
        'manufacturer': 'Seat',
        'model': 'Leon 1',
        'year': 2003,
        'body': 'hatchback',
        'length': 4140,
        'mileage': 205000,
        'weight': 1700,
        'name': 'ProjectCar'
    }

    return d


@pytest.fixture(scope="session")
def mock_log_entry() -> dict:
    entry = {"desc": "Engine Checkup",
             "date": "09-03-1964",
             "mileage": 1404,
             "category": EntryCategory.check,
             "tags": [],
             }

    return entry


@pytest.fixture(scope="session")
def mock_component(mock_log_entry) -> CarComponent:
    comp = CarComponent("TestComponent")
    comp.create_entry(mock_log_entry)

    return comp


@pytest.fixture(scope="session")
def mock_component_clean(mock_log_entry) -> CarComponent:
    comp = CarComponent("TestComponent")
    return comp


@pytest.fixture(scope="session")
def mock_component_collection() -> ComponentCollection:
    sp = CarComponent("Spark Plug")
    v = CarComponent("Valves")
    bat = CarComponent("Battery")

    engine_c = ComponentCollection("Engine")
    elec_c = ComponentCollection("Power")

    engine_c.children.append(sp)
    elec_c.children.append(bat)
    engine_c.children.append(elec_c)
    engine_c.children.append(v)

    return engine_c


@pytest.fixture
def mock_car_directory(tmp_path, directory_manager, mock_car_info) -> dict[str, pathlib.Path]:
    car_info = CarInfo(**mock_car_info)
    path = tmp_path.joinpath(car_info.name)
    car_to_add = Car(car_info, path=path)

    directory_manager.car_save_dir = tmp_path

    directory_manager.create_car_directory(car_to_add)

    return {'car_dir': path,
            'info_path': path.joinpath(car_to_add.car_info.path)}


@pytest.fixture
def directory_manager() -> DirectoryManager:
    return DirectoryManager(JSONFiledataManager())
