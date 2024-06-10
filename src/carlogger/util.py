"""General utility functions"""
import dataclasses
import datetime
import os
import pathlib
import time
import re
import uuid

from dataclasses import fields
from pathlib import Path

from carlogger.const import CARS_PATH, TODAY, ITEM_FILE_EXTENSIONS, InvalidFileExtension, INVALID_FILE_EXTENSION_MESSAGE


# ===== General ===== #

def dict_diff(dict1: dict, dict2: dict) -> dict:
    """Compare two dictionaries and return first dictionary only with values that are unique."""
    return {k: v for k, v in dict1.items() if dict2[k] != v}


# ===== Items ===== #

def is_scheduled_entry(entry) -> bool:
    return entry.__class__.__name__ == 'ScheduledLogEntry'


def sort_key_is_attrib(key: str, item) -> bool:
    try:
        getattr(item, key)
        return True
    except Exception:
        return False


def get_all_required_fields(item_class) -> list[str]:
    item_fields = fields(item_class)
    init_fields = [f.name for f in item_fields
                   if f.init and f.default is dataclasses.MISSING
                   and f.default_factory is dataclasses.MISSING
                   and f.name[0] != '_']

    return init_fields or []


def is_valid_entry_id(entry_id: str) -> bool:
    """Checks whether passed string is a valid entry id."""
    try:
        uuid.UUID(entry_id, version=1)
        return True
    except TypeError:
        return False


def get_all_class_properties(item_instance) -> list[str]:
    """Returns list of names of all instance variables except magic and private ones."""
    return [attr for attr in dir(item_instance) if
            not callable(getattr(item_instance, attr)) and not attr.startswith("__") and not attr.startswith("_")]


# ===== SAVING ===== #

def create_car_dir_path(car_info: dict) -> Path:
    name = car_info['name'].replace(" ", "_")
    path = CARS_PATH.joinpath(f"{name}")
    return path


def get_car_dirs(cars_save_path=CARS_PATH) -> list[str]:
    car_dirs = filter(lambda x: os.path.isdir(cars_save_path.joinpath(x)),
                      os.listdir(cars_save_path))
    return list(car_dirs)


def is_valid_file_extension(path: pathlib.Path | str) -> bool:
    clamped_path = pathlib.Path(path)
    extension = clamped_path.suffix
    return extension in ITEM_FILE_EXTENSIONS


def check_file_extension_validity(path: pathlib.Path | str):
    clamped_path = pathlib.Path(path)
    extension = clamped_path.suffix

    if extension not in ITEM_FILE_EXTENSIONS:
        raise InvalidFileExtension(INVALID_FILE_EXTENSION_MESSAGE.format(extension, ITEM_FILE_EXTENSIONS), extension)


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
    """Format time string to a datetime date class"""
    date_tuple = tuple([int(x) for x in date.split('-')])
    return datetime.date(year=date_tuple[2], month=date_tuple[1], day=date_tuple[0])


def is_date(date: str) -> bool:
    """NOTE: this is a soft check, it only checks whether passed string is a date of 'xx-xx-xxxx' format,
    it does NOT check for validity of day, month and year numbers!"""
    regex = re.fullmatch(r'^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-(\d{4})$', date)
    return regex is not None


def is_date_range(date: str) -> bool:
    """NOTE: this is a soft check, it only checks whether passed string is a date of 'xx-xx-xxxx' format,
    it does NOT check for validity of day, month and year numbers!"""
    regex = re.fullmatch(r'^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-(\d{4})-'
                         r'(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-(\d{4})$', date)
    return regex is not None


def is_date_in_range(date: str, date_range: str) -> bool:
    date = date_string_to_date(date)
    upper = date_string_to_date(date_range[:10:])
    lower = date_string_to_date(date_range[11::])
    return lower >= date >= upper


def days_between_date_strings(date: str, date2: str) -> int:
    """Takes two date strings formatted as 'xx-xx-xxx' and returns number od days between them"""
    date = date_string_to_date(date)
    days = date - date_string_to_date(date2)
    return days.days


def date_n_days_from_now(days: int) -> str:
    """Returns a string date x days from now"""
    date_today = date_string_to_date(TODAY)
    new_date = date_today - datetime.timedelta(days=days * -1)
    new_date = (new_date.day, new_date.month, new_date.year)
    return format_tuple_to_date_string(new_date)
