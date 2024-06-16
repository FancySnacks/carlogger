"""Constant variables"""

from __future__ import annotations

import pathlib

from datetime import datetime
from typing import Union, TYPE_CHECKING

ITEM = None

if TYPE_CHECKING:
    from carlogger.items.car import Car
    from carlogger.items.car_info import CarInfo
    from carlogger.items.component_collection import ComponentCollection
    from carlogger.items.car_component import CarComponent
    from carlogger.items.log_entry import LogEntry, ScheduledLogEntry

    ITEM = Union[Car, CarInfo, ComponentCollection, CarComponent, LogEntry, ScheduledLogEntry]

PATH = pathlib.Path(__file__).parent.parent.parent
CARS_PATH = PATH.joinpath("save")

TODAY = datetime.today().date().strftime("%d-%m-%Y")

ITEM_FILE_EXTENSIONS = ['.txt', '.json', '.csv', '.html', '.yaml']
INVALID_FILE_EXTENSION_MESSAGE = "'{0}' is not a valid file extension! " \
                                 "Did you mean one of these? {1}"


class InvalidFileExtension(Exception):
    def __init__(self, message, val, *args):
        self.message = message
        self.val = val
        super(InvalidFileExtension, self).__init__(message, val, *args)
