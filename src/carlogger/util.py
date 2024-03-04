"""General utility functions"""

import os
import time

from pathlib import Path

from carlogger.const import CARS_PATH


# ===== SAVING ===== #

def create_car_dir_path(car_info: dict) -> Path:
    name = car_info['name'].replace(" ", "_")
    path = CARS_PATH.joinpath(f"{name}")
    return path


def get_car_dirs() -> list[str]:
    car_dirs = filter(lambda x: os.path.isdir(CARS_PATH.joinpath(x)),
                      os.listdir(CARS_PATH))
    return list(car_dirs)


# ===== DATE ===== #

def format_date_struct_to_tuple(current_time: time.struct_time) -> tuple[int, int, int]:
    """Format time.localtime() to a usable tuple containing day, month and year."""
    return current_time.tm_mday, current_time.tm_mon, current_time.tm_year


def format_tuple_to_date_string(date: tuple[int, int, int]) -> str:
    """Format time tuple to a string format of 'dd-mm-yyyy'"""
    stringify = [f"{x:02d}" for x in date]
    return "-".join(stringify)


def format_date_string_to_tuple(date: str) -> tuple[int]:
    """Format time string to a three int tuple."""
    return tuple([int(x) for x in date.split('-')])
