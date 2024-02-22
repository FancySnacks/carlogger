import os

from carlogger.filedata_manager import JSONFiledataManager


def test_saves_data_as_json(mock_component, tmp_path):
    filename = mock_component.name + ".json"
    saver = JSONFiledataManager()
    saver.save_file(mock_component, f"{tmp_path}/")

    files: list[str] = os.listdir(".")

    assert filename in files


def test_save_and_load_json(mock_component, tmp_path):
    data: dict = mock_component.to_json()

    filename = mock_component.name + ".json"
    saver = JSONFiledataManager()
    saver.save_file(mock_component, f"{tmp_path}/")

    loaded_data = saver.load_file(f"{tmp_path}/{filename}")

    assert data == loaded_data
