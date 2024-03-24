"""A certain car component or part that has maintenance logs."""

import pathlib
import uuid

from dataclasses import dataclass, field

from carlogger.const import ADD_ENTRY_SUCCESS, REMOVE_ENTRY_SUCCESS_ID, REMOVE_ENTRY_FAILURE_ID, \
    REMOVE_ENTRY_FAILURE_INDEX, REMOVE_ENTRY_SUCCESS_INDEX
from carlogger.items.log_entry import LogEntry
from carlogger.items.entry_category import EntryCategory


@dataclass
class CarComponent:
    """A certain car component or part that has maintenance logs."""

    name: str
    log_entries: list[LogEntry] = field(init=False, default_factory=list)
    search_tags: set[str] = field(init=False, default_factory=set)
    path: str = ""

    def __post_init__(self):
        self.search_tags.add(self.name)
        self.path = pathlib.Path(self.path)

    def create_entry(self, entry_data: dict) -> str:
        """Creates a new entry adding it to the list and returns its unique id."""

        new_entry = LogEntry(desc=entry_data['desc'],
                             date=entry_data['date'],
                             mileage=entry_data['mileage'],
                             category=EntryCategory(entry_data['category']),
                             tags=entry_data['tags'],
                             component=self,
                             _id=str(uuid.uuid1()))
        self.log_entries.append(new_entry)

        print(ADD_ENTRY_SUCCESS.format(id=new_entry.id))
        self._add_search_tags_from_entry(new_entry)

        return new_entry.id

    def create_entry_from_file(self, entry_data: dict) -> str:
        """Creates a new entry adding it to the list without creating new id."""

        new_entry = LogEntry(desc=entry_data['desc'],
                             date=entry_data['date'],
                             mileage=entry_data['mileage'],
                             category=EntryCategory(entry_data['category']),
                             tags=entry_data['tags'],
                             component=self,
                             _id=entry_data['id'])
        self.log_entries.append(new_entry)

        self._add_search_tags_from_entry(new_entry)

        return new_entry.id

    def update_entry(self, entry_id: str, changes: dict):
        """Update values of log entry with specified unique id hash. \n
        'entry_changes' is a dictionary that contains only keys that are to be overwritten and their new values.\n
        Unique ID of updated entry cannot be changed."""

        entry_to_update = self.get_entry_by_id(entry_id)

        for k, v in changes.items():
            if k not in ("_id", "id"):
                entry_to_update.to_json()[k] = v

        self._add_search_tags_from_entry(entry_to_update)

    def delete_entry_by_id(self, entry_id: str):
        """Delete log entry given it's unique id hash."""
        entry_to_delete = self.get_entry_by_id(entry_id)

        if entry_to_delete:
            self.log_entries.remove(entry_to_delete)
            print(REMOVE_ENTRY_SUCCESS_ID.format(id=entry_id))
        else:
            print(REMOVE_ENTRY_FAILURE_ID.format(id=entry_id, component=self.name))

    def delete_entry_by_index(self, entry_index: int = -1):
        """Removes log entry from list at target index, removes last one by default."""
        try:
            self.log_entries.pop(entry_index)
            print(REMOVE_ENTRY_SUCCESS_INDEX.format(index=entry_index))
        except IndexError:
            print(REMOVE_ENTRY_FAILURE_INDEX.format(index=entry_index, component=self.name))

    def get_entry_by_id(self, entry_id: str) -> LogEntry | None:
        """Return log entry by its unique id hash."""
        i = 0

        while i < len(self.log_entries):
            if self.log_entries[i].id == entry_id:
                return self.log_entries[i]
            else:
                i += 1

        print("No entry with given id has been found")

    def to_json(self) -> dict:
        """Returns object properties as JSON-serializable dictionary."""
        d = {'name': self.name,
             'log_entries': [entry.to_json() for entry in self.log_entries],
             'search_tags': list(self.search_tags),
             }

        return d

    def get_target_path(self, extension: str) -> str:
        """Extension without the dot"""
        return self.path.joinpath(f"{self.name.replace(' ', '_')}.{extension}")

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        result = f"{self.name} ({len(self.log_entries)}): \n"

        for entry in self.log_entries:
            result += f"{entry.get_formatted_info()}\n"

        return result

    def _add_search_tags_from_entry(self, entry: LogEntry):
        string_tags = entry.desc, *entry.tags, entry.component.name, entry.category, entry.date

        for tag in string_tags:
            self.search_tags.add(tag)
