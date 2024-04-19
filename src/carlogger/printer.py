"""Printer class for printing informative strings into console."""

from enum import StrEnum


class Message(StrEnum):
    ADD_SUCCESS = "SUCCESS: {name} was added to {relation}"
    ADD_FAIL = "FAIL: Failed to add {name} to {relation} {reason}"
    DEL_SUCCESS = "SUCCESS: {name} was deleted successfully from {relation}"
    DEL_FAIL = "FAIL: Failed to delete {name} in {relation} {reason}"
    READ_FAIL = "FAIL: {name} was not found in {relation}"
    UPDATE_SUCCESS = "SUCCESS: {name} was updated"
    UPDATE_FAIL = "FAIL: Failed to update {name} {reason}"


class Printer:
    @classmethod
    def print_msg(cls, item, msg_type: str, **values):
        reason = values.get('reason')
        if not reason:
            values['reason'] = ''

        buffer_str = getattr(Message, msg_type).format(**values)
        print(buffer_str)
