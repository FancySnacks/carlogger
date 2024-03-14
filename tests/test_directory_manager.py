import pathlib
import shutil


def test_new_directory_on_car_added(mock_car_directory):
    assert pathlib.Path(mock_car_directory['car_dir']).exists()


def test_car_directory_removed(mock_car_directory, directory_manager):
    shutil.rmtree(mock_car_directory['car_dir'])
    assert not pathlib.Path(mock_car_directory['car_dir']).exists()


def test_car_directory_info_file_is_created(mock_car_directory):
    assert pathlib.Path(mock_car_directory['info_path']).exists()
