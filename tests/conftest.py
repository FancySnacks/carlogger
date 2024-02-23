import pytest

from carlogger.car_component import  CarComponent
from carlogger.component_collection import ComponentCollection
from carlogger.entry_category import EntryCategory


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
