import pytest

from carlogger.car_component import CarComponent
from carlogger.component_collection import ComponentCollection
from carlogger.entry_category import EntryCategory
from carlogger.directory_manager import DirectoryManager
from carlogger.filedata_manager import JSONFiledataManager


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
        'name': 'Daily'
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


@pytest.fixture(scope="session")
def directory_manager() -> DirectoryManager:
    return DirectoryManager(JSONFiledataManager())
