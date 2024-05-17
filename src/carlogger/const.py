"""Constant variables"""

import pathlib
from datetime import datetime

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
