"""Constant variables"""

import pathlib

PATH = pathlib.Path(__file__).parent.parent.parent
CARS_PATH = PATH.joinpath("save")


# ==== STDOUT ==== #
ADD_CAR_SUCCESS = "SUCCESS: '{name}' directory was successfully created at: '{path}'"
ADD_CAR_FAILURE = "ERROR: '{name}' was not created as directory with exact name already exists at: '{path}'"
