import pytest

import os

from carlogger.car import Car
from carlogger.car_info import CarInfo


def test_new_directory_on_car_added(tmp_path, directory_manager, mock_car_info):
    car_info = CarInfo(**mock_car_info)
    path = tmp_path.joinpath(car_info.name)
    car_to_add = Car(car_info, path=path)

    directory_manager.create_car_directory(car_to_add)

    assert car_info.name in os.listdir(tmp_path)


def test_car_directory_removed(tmp_path, directory_manager, mock_car_info):
    car_info = CarInfo(**mock_car_info)
    path = tmp_path.joinpath(car_info.name)
    car_to_add = Car(car_info, path=path)

    directory_manager.create_car_directory(car_to_add)
    directory_manager.remove_car_directory(car_to_add)

    assert car_info.name not in os.listdir(tmp_path)


def test_car_directory_info_file_is_created(tmp_path, directory_manager, mock_car_info):
    car_info = CarInfo(**mock_car_info)
    path = tmp_path.joinpath(car_info.name)
    car_to_add = Car(car_info, path=path)

    directory_manager.create_car_directory(car_to_add)

    assert f"{car_info.name}.{directory_manager.data_manager.suffix}" in os.listdir(tmp_path.joinpath(car_info.name))
