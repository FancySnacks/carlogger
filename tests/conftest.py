import pytest
import pathlib

from carlogger.items.car import Car
from carlogger.items.car_component import CarComponent
from carlogger.items.car_info import CarInfo
from carlogger.items.component_collection import ComponentCollection
from carlogger.items.entry_category import EntryCategory
from carlogger.directory_manager import DirectoryManager
from carlogger.filedata_manager import JSONFiledataManager
from carlogger.const import TODAY


with open(pathlib.Path.cwd().joinpath("tests/add_arg_test"), "r") as f:
    commands = [c.replace("\n", "").replace('"', "").split() for c in f.readlines()]
    keys = ['car', 'collection', 'nested', 'nestedtwo', 'component', 'nestedcomponent', 'entry']
    args = list(zip(keys, commands))

ADD_ARGS = {k: v for k, v in args}
ADD_ARGS['entry'] = ['carlogger', 'add', 'entry', '--car', 'CarTestPytest', '--collection', 'Engine',
                     '--component', 'Spark_Plug', '--desc', 'Replaced all spark plugs.',
                     '--mileage', '198000', '--category', 'swap', '--custom', 'part=Bosch Double Iridium']

with open(pathlib.Path.cwd().joinpath("tests/delete_arg_test"), "r") as f:
    commands = [c.replace("\n", "").replace('"', "").split() for c in f.readlines()]
    keys = ['entry', 'component', 'nestedcomponent', 'nestedtwo', 'nested', 'collection', 'car']
    args = list(zip(keys, commands))

DEL_ARGS = {k: v for k, v in args}

with open(pathlib.Path.cwd().joinpath("tests/read_arg_test"), "r") as f:
    commands = [c.replace("\n", "").replace('"', "").split() for c in f.readlines()]
    keys = ['car', 'collection', 'nested_coll', 'component', 'coll_all', 'comp_all', 'entry']
    args = list(zip(keys, commands))

READ_ARGS = {k: v for k, v in args}

with open(pathlib.Path.cwd().joinpath("tests/update_arg_test"), "r") as f:
    commands = [c.replace("\n", "").replace('"', "").split() for c in f.readlines()]
    keys = ['component', 'collection', 'car']
    args = list(zip(keys, commands))

UPDATE_ARGS = {k: v for k, v in args}

with open(pathlib.Path.cwd().joinpath("tests/export_arg_test"), "r") as f:
    commands = [c.replace("\n", "").replace('"', "").split() for c in f.readlines()]
    keys = ['car', 'collection', 'component']
    args = list(zip(keys, commands[1:-1:]))

EXPORT_ARGS = {k: v for k, v in args}

with open(pathlib.Path.cwd().joinpath("tests/import_arg_test"), "r") as f:
    commands = [c.replace("\n", "").replace('"', "").split() for c in f.readlines()]
    keys = ['car', 'collection', 'cmp', 'component']
    args = list(zip(keys, commands[:-3:]))

IMPORT_ARGS = {k: v for k, v in args}


@pytest.fixture
def add_cmd() -> dict:
    return ADD_ARGS


@pytest.fixture
def delete_cmd() -> dict:
    return DEL_ARGS


@pytest.fixture
def read_cmd() -> dict:
    return READ_ARGS


@pytest.fixture
def update_cmd() -> dict:
    return UPDATE_ARGS


@pytest.fixture
def export_cmd() -> dict:
    return EXPORT_ARGS


@pytest.fixture
def import_cmd() -> dict:
    return IMPORT_ARGS


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


@pytest.fixture
def mock_car_dict_list() -> list[dict]:
    car_1 = {
        'manufacturer': 'Fiat',
        'model': '500',
        'year': 2017,
        'body': 'hatchback',
        'length': 4140,
        'mileage': 13500,
        'weight': 1700,
        'name': 'NewPurchase'
    }

    car_2 = {
        'manufacturer': 'Toyota',
        'model': 'Celica',
        'year': 2003,
        'body': 'coupe',
        'length': 4140,
        'mileage': 221387,
        'weight': 1700,
        'name': 'ProjectCar'
    }

    return [car_1, car_2]


@pytest.fixture
def mock_cars_full(mock_car_dict_list) -> list[Car]:
    cars = [Car(CarInfo(**c)) for c in mock_car_dict_list]
    return cars


@pytest.fixture
def mock_log_entry() -> dict:
    entry = {"desc": "Engine Checkup",
             "date": "09-03-1964",
             "mileage": 1404,
             "category": EntryCategory.check,
             "tags": [],
             }

    return entry


@pytest.fixture
def mock_entry_dict_list() -> list[dict]:
    entry_1 = {"desc": "Engine Checkup",
               "date": "09-03-1964",
               "mileage": 1404,
               "category": EntryCategory.check,
               "tags": [],
               }

    entry_2 = {"desc": "Engine Checkup",
               "date": TODAY,
               "mileage": 1404,
               "category": EntryCategory.check,
               "tags": [],
               }

    return [entry_1, entry_2]


@pytest.fixture
def mock_scheduled_log_entry() -> dict:
    entry = {"desc": "Engine Checkup",
             "date": "12-06-1964",
             "mileage": 2380,
             "category": EntryCategory.check,
             "tags": [],
             "repeating": True,
             "frequency": 10,
             "rule": "date",
             }

    return entry


@pytest.fixture
def mock_component(mock_log_entry) -> CarComponent:
    comp = CarComponent("TestComponent")
    comp.create_entry(mock_log_entry)

    return comp


@pytest.fixture
def mock_component_clean(mock_log_entry) -> CarComponent:
    comp = CarComponent("TestComponent")
    return comp


@pytest.fixture
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
def mock_car(mock_car_info) -> Car:
    car_info = CarInfo(**mock_car_info)
    car = Car(car_info)
    return car


@pytest.fixture
def mock_car_full(mock_car_info, mock_log_entry) -> Car:
    car_info = CarInfo(**mock_car_info)
    car = Car(car_info)
    coll = car.create_collection('TestCollection')
    comp = coll.create_component('TestComponent')
    comp.create_entry(**mock_log_entry)
    return car


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
