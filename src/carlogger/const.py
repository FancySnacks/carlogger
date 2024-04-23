"""Constant variables"""

import pathlib
from datetime import datetime

PATH = pathlib.Path(__file__).parent.parent.parent
CARS_PATH = PATH.joinpath("save")

TODAY = datetime.today().date().strftime("%d-%m-%Y")
