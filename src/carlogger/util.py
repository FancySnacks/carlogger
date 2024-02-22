"""General utility functions"""

import time


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
