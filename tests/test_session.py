from carlogger.session import AppSession


def test_car_is_removed(directory_manager, mock_car_directory, tmp_path):
    car_name = mock_car_directory['car_dir'].name

    directory_manager.car_save_dir = tmp_path
    session = AppSession(directory_manager)
    session.load_car_dir(car_name)
    session.delete_car(car_name)

    assert len(session.cars) == 0


def test_collection_is_removed(directory_manager, mock_car_directory, tmp_path):
    car_name = mock_car_directory['car_dir'].name

    directory_manager.car_save_dir = tmp_path
    session = AppSession(directory_manager)
    session.load_car_dir(car_name)

    session.selected_car.create_collection('Test')
    prev_count = len(session.selected_car.collections)

    session.selected_car.delete_collection('Test')
    next_count = len(session.selected_car.collections)

    assert prev_count != next_count


def test_component_is_removed(directory_manager, mock_car_directory, tmp_path):
    car_name = mock_car_directory['car_dir'].name

    directory_manager.car_save_dir = tmp_path
    session = AppSession(directory_manager)
    session.load_car_dir(car_name)

    session.selected_car.create_collection('Test')
    session.add_new_component(car_name, 'Test', 'SparkPlug')
    prev_count = len(session.selected_car.collections[0].children)

    session.delete_component(car_name, 'Test', 'SparkPlug')
    next_count = len(session.selected_car.collections[0].children)

    assert prev_count != next_count


def test_entry_is_removed_by_index(directory_manager, mock_car_directory, tmp_path, mock_log_entry):
    car_name = mock_car_directory['car_dir'].name

    directory_manager.car_save_dir = tmp_path
    session = AppSession(directory_manager)
    session.load_car_dir(car_name)

    session.selected_car.create_collection('Test')
    session.add_new_component(car_name, 'Test', 'SparkPlug')
    session.add_new_entry(car_name, 'Test', 'SparkPlug', mock_log_entry)

    prev_count = len(session.get_car_by_name(car_name).get_component_by_name('SparkPlug').log_entries)

    session.delete_entry_by_index(car_name, 'SparkPlug', 0)
    next_count = len(session.get_car_by_name(car_name).get_component_by_name('SparkPlug').log_entries)

    assert prev_count != next_count


def test_entry_is_removed_by_unique_id(directory_manager, mock_car_directory, tmp_path, mock_log_entry):
    car_name = mock_car_directory['car_dir'].name

    directory_manager.car_save_dir = tmp_path
    session = AppSession(directory_manager)
    session.load_car_dir(car_name)

    session.selected_car.create_collection('Test')
    session.add_new_component(car_name, 'Test', 'SparkPlug')
    session.add_new_entry(car_name, 'Test', 'SparkPlug', mock_log_entry)

    entries = session.get_car_by_name(car_name).get_component_by_name('SparkPlug').log_entries

    prev_count = len(entries)
    entry_id = entries[0].id

    session.delete_entry_by_id(car_name, 'SparkPlug', entry_id)
    next_count = len(session.get_car_by_name(car_name).get_component_by_name('SparkPlug').log_entries)

    assert prev_count != next_count
