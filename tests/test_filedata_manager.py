import os

from carlogger.filedata_manager import JSONFiledataManager


def test_saves_entry_data_as_json(mock_component, tmp_path):
    filename = mock_component.name + ".json"
    saver = JSONFiledataManager()
    saver.save_file(mock_component, f"{tmp_path}/{filename}")

    files: list[str] = os.listdir(tmp_path)

    assert filename in files


def test_save_and_load_entry_data_json(mock_component, tmp_path):
    data: dict = mock_component.to_json()

    filename = mock_component.name + ".json"
    saver = JSONFiledataManager()
    saver.save_file(mock_component, f"{tmp_path}/{filename}")

    loaded_data = saver.load_file(f"{tmp_path}/{filename}")

    assert data == loaded_data


def test_saves_collection_as_json(mock_component_collection, tmp_path):
    filename = mock_component_collection.name + ".json"
    saver = JSONFiledataManager()
    saver.save_file(mock_component_collection, f"{tmp_path}/{filename}")

    files: list[str] = os.listdir(tmp_path)

    assert filename in files


def test_save_and_load_collection_json(mock_component_collection, tmp_path):
    data: dict = mock_component_collection.to_json()

    filename = mock_component_collection.name + ".json"
    saver = JSONFiledataManager()
    saver.save_file(mock_component_collection, f"{tmp_path}/{filename}")

    loaded_data = saver.load_file(f"{tmp_path}/{filename}")

    assert data == loaded_data
