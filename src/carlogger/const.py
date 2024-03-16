"""Constant variables"""

import pathlib

PATH = pathlib.Path(__file__).parent.parent.parent
CARS_PATH = PATH.joinpath("save")


# ==== STDOUT ==== #
ADD_CAR_SUCCESS = "SUCCESS: '{name}' directory was successfully created at: '{path}'"
ADD_CAR_FAILURE = "ERROR: '{name}' was not created as directory with exact name already exists at: '{path}'"
REMOVE_CAR_SUCCESS = "SUCCESS: '{name}' directory was removed"
REMOVE_CAR_FAILURE = "ERROR: '{name}' directory was NOT removed"

ADD_COLLECTION_SUCCESS = "SUCCESS: '{name}' collection was successfully created"
ADD_COLLECTION_FAILURE = "ERROR: '{name}' was not created as collection with exact name already exists in '{car}'"

ADD_COMPONENT_SUCCESS = "SUCCESS: '{name}' component was successfully created"
ADD_COMPONENT_FAILURE = "ERROR: '{name}' was not created as component with exact name already exists " \
                        "in '{collection}'"

ADD_ENTRY_SUCCESS = "SUCCESS: Entry of ID: '{id}' was successfully created"
