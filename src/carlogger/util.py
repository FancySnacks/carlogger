"""General utility functions"""
import datetime
import os
import time
import re
import uuid

from pathlib import Path

from carlogger.const import CARS_PATH


# ===== SAVING ===== #

def is_valid_entry_id(entry_id: str) -> bool:
    """Checks whether passed string is a valid entry id."""
    try:
        test = uuid.UUID(entry_id, version=1)
        return True
    except TypeError:
        return False



# ===== SAVING ===== #

def create_car_dir_path(car_info: dict) -> Path:
    name = car_info['name'].replace(" ", "_")
    path = CARS_PATH.joinpath(f"{name}")
    return path


def get_car_dirs(cars_save_path=CARS_PATH) -> list[str]:
    car_dirs = filter(lambda x: os.path.isdir(cars_save_path.joinpath(x)),
                      os.listdir(cars_save_path))
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


def date_string_to_date(date: str) -> datetime.date:
    """Format time string to a datetime.date class"""
    date_tuple = tuple([int(x) for x in date.split('-')])
    return datetime.date(year=date_tuple[2], month=date_tuple[1], day=date_tuple[0])


def is_date(date: str) -> bool:
    """NOTE: this is a soft check, it only checks whether passed string is a date of 'xx-xx-xxxx' format,
    it does NOT check for validity of day, month and year numbers!"""
    regex = re.fullmatch(r'^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-(\d{4})$', date)
    return regex is not None
