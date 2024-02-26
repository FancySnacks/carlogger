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
    name: str = ""

    def __post_init__(self):
        if self.name == "":
            self.name = self.get_full_name()

    def get_full_name(self) -> str:
        return f"{self.manufacturer} {self.model}"

    def to_json(self) -> dict:
        """Return a json-serializable dictionary of the class."""
        return vars(self)
