from carlogger.items.car_component import CarComponent


def test_get_function_returns_entry_logs(mock_log_entry, mock_component_collection):
    c = CarComponent("Engine Oil")
    c.create_entry(mock_log_entry)

    mock_component_collection.components.append(c)
    logs = mock_component_collection.get_all_entry_logs()

    assert len(logs) > 0
