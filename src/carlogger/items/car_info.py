"""Car info; manufacturer, year of make, equipment version, weight, classification etc."""

from dataclasses import dataclass, field


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
    path: str = ""
    custom_info: dict[str, ...] = field(default_factory=dict)

    def __post_init__(self):
        if self.name == "":
            self.name = self.get_full_name()

    def filter_options(self) -> list[str]:
        return ['name', 'manufacturer', 'model', 'year', 'mileage', 'log #', 'latest'] + list(self.custom_info.keys())

    def get_full_name(self) -> str:
        return f"{self.manufacturer} {self.model}"

    def to_json(self) -> dict:
        """Return a json-serializable dictionary of the class."""
        self.path = str(self.path)
        return vars(self)
