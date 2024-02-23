from carlogger.log_entry import LogEntry
from carlogger.car_component import CarComponent


def test_get_function_returns_only_car_parts(mock_component_collection):
    parts = mock_component_collection.get_all_components(mock_component_collection.children)
    filtered_list = list(filter(lambda x: type(x) == CarComponent, parts))

    assert len(parts) == len(filtered_list)


def test_get_function_returns_entry_logs(mock_log_entry, mock_component_collection):
    c = CarComponent("Engine Oil")
    c.create_entry(mock_log_entry)

    mock_component_collection.children.append(c)

    logs = mock_component_collection.get_all_log_entries(mock_component_collection.children)

    assert len(logs) > 0


def test_get_function_returns_only_entry_logs(mock_log_entry, mock_component_collection):
    c = CarComponent("Engine Oil")
    c.create_entry(mock_log_entry)

    mock_component_collection.children.append(c)

    logs = mock_component_collection.get_all_log_entries(mock_component_collection.children)
    filtered_list = list(filter(lambda x: type(x) == LogEntry, logs))

    assert len(logs) == len(filtered_list)
