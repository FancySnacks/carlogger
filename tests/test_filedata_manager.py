import os

from carlogger.filedata_manager import JSONFiledataManager


def test_saves_data_as_json(mock_component):
    filename = mock_component.name + ".json"
    saver = JSONFiledataManager()
    saver.save_file(mock_component, "./")

    files: list[str] = os.listdir(".")

    assert filename in files


def test_loads_data_as_json(mock_component):
    filename = mock_component.name + ".json"
    saver = JSONFiledataManager()
    data = saver.load_file(f"./{filename}")

    assert data is not None


def test_save_and_load_json(mock_component):
    data: dict = mock_component.to_json()

    filename = mock_component.name + ".json"
    saver = JSONFiledataManager()
    saver.save_file(mock_component, "./")

    loaded_data = saver.load_file(f"./{filename}")

    assert data == loaded_data
