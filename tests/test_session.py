import os

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


def test_collection_children_are_removed_with_it(directory_manager, mock_car_directory, tmp_path):
    car_name = mock_car_directory['car_dir'].name

    directory_manager.car_save_dir = tmp_path
    session = AppSession(directory_manager)
    session.load_car_dir(car_name)

    session.add_new_collection(car_name, 'Test')
    session.add_new_component(car_name, 'Test', 'ComponentTest')

    session.delete_collection(car_name, 'Test')

    assert len(os.listdir(mock_car_directory['car_dir'].joinpath("components"))) == 0


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

    session.delete_entry_by_id(car_name, entry_id)
    next_count = len(session.get_car_by_name(car_name).get_component_by_name('SparkPlug').log_entries)

    assert prev_count != next_count


def test_car_children_are_cleared(directory_manager, mock_car_directory, tmp_path, mock_log_entry):
    car_name = mock_car_directory['car_dir'].name
    directory_manager.car_save_dir = tmp_path

    session = AppSession(directory_manager)
    session.load_car_dir(car_name)

    session.selected_car.create_collection('Test')
    session.add_new_component(car_name, 'Test', 'SparkPlug')
    session.add_new_entry(car_name, 'Test', 'SparkPlug', mock_log_entry)

    session.delete_car_children(session.selected_car)

    assert sum([len(session.selected_car.collections), len(session.selected_car.get_all_entry_logs())]) == 0


def test_collection_children_are_cleared(directory_manager, mock_car_directory, tmp_path, mock_log_entry):
    car_name = mock_car_directory['car_dir'].name
    directory_manager.car_save_dir = tmp_path

    session = AppSession(directory_manager)
    session.load_car_dir(car_name)

    parent_coll = session.selected_car.create_collection('Engine')
    parent_coll.create_component('SparkPlug')
    session.add_new_nested_collection(car_name, 'Turbocharger', 'Engine')
    session.add_new_entry(car_name, 'Engine', 'SparkPlug', mock_log_entry)

    session.delete_collection_children(car_name, parent_coll)

    assert len(parent_coll.children) == 0


def test_component_children_are_cleared(directory_manager, mock_car_directory, tmp_path, mock_log_entry):
    car_name = mock_car_directory['car_dir'].name
    directory_manager.car_save_dir = tmp_path

    session = AppSession(directory_manager)
    session.load_car_dir(car_name)

    parent_coll = session.selected_car.create_collection('Engine')
    comp = parent_coll.create_component('SparkPlug')
    session.add_new_entry(car_name, 'Engine', 'SparkPlug', mock_log_entry)
    session.add_new_entry(car_name, 'Engine', 'SparkPlug', mock_log_entry)

    session.delete_component_children(comp, session.selected_car)

    assert len(comp.log_entries) == 0
