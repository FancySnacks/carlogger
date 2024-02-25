"""Car info; manufacturer, year of make, equipment version, weight, classification etc."""

from dataclasses import dataclass


@dataclass
class CarInfo:
    manufacturer: str
    model: str
    year: int
    mileage: int
    body: str
    length: int
    weight: int

    def to_json(self) -> dict:
        """Return a json-serializable dictionary of the class."""
        return vars(self)
