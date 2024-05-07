"""Represents a single part with reference to it's parent LogEntry."""

from dataclasses import dataclass, field

from carlogger.items.log_entry import LogEntry


@dataclass(order=True)
class Part:
    name: str
    parent_entry_id: str
    custom_info: dict[str, ...] = field(default_factory=dict)

    def to_json(self) -> dict:
        d = {'name': self.name,
             'parent_entry_id': self.parent_entry_id,
             'custom_info': self.custom_info,
             }

        return d
