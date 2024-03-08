"""Type of work done on a specific component"""

from enum import StrEnum, auto


class EntryCategory(StrEnum):
    """
    `check` - simple component check, can be created independently by user OR as a result of scheduled check \n
    `part_swap` - new part inserted, parent CarComponent will update the currently displayed part \n
    `repair` - current part was repaired, currently equipped part is displayed the same \n
    `fluid_change` - old fluid drained, new fluid added \n
    `fluid_add` - topped current fluid up \n
    `other` - anything that doesn't fit above categories \n
    """
    check = auto()
    part_swap = auto()
    repair = auto()
    fluid_change = auto()
    fluid_add = auto()
    other = auto()

    @classmethod
    def get_categories(cls) -> list[str]:
        return [member.value for member in cls]
