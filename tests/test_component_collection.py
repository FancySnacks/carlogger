from carlogger.items.log_entry import LogEntry
from carlogger.items.car_component import CarComponent
from carlogger.items.component_collection import ComponentCollection


def test_get_function_returns_only_car_parts(mock_component_collection):
    mock_component_collection.create_component('Test')
    parts = mock_component_collection.get_all_components()

    assert len(parts) == len(parts)


def test_get_function_returns_entry_logs(mock_log_entry, mock_component_collection):
    c = CarComponent("Engine Oil")
    c.create_entry(mock_log_entry)

    mock_component_collection.components.append(c)
    logs = mock_component_collection.get_all_log_entries()

    assert len(logs) > 0
