"""A certain car component or part that has maintenance logs."""

from __future__ import annotations

import pathlib
import uuid

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from carlogger.items.log_entry import LogEntry, ScheduledLogEntry
from carlogger.items.part import Part
from carlogger.items.entry_category import EntryCategory
from carlogger.printer import Printer
from carlogger.const import TODAY

if TYPE_CHECKING:
    from carlogger.items.component_collection import ComponentCollection


@dataclass(order=True)
class CarComponent:
    """A certain car component or part that has maintenance logs."""

    name: str
    desc: str = ""

    log_entries: list[LogEntry] = field(init=False, default_factory=list)
    scheduled_log_entries: list[ScheduledLogEntry] = field(init=False, default_factory=list)

    current_part: Part = field(init=False, default=None)
    part_list: list[Part] = field(init=False, default_factory=list)

    current_mileage: int = field(init=False, default=0)
    parent: ComponentCollection = field(init=False, default=None)
    custom_info: dict[str, ...] = field(default_factory=dict)

    path: str = ""
    _sort_index: str = field(init=False, repr=False, default='')

    def __post_init__(self):
        self.path = pathlib.Path(self.path)
        self._sort_index = self.name

    @property
    def latest_entry(self) -> LogEntry:
        return self.log_entries[-1]

    @property
    def children(self) -> list[LogEntry, ScheduledLogEntry]:
        return self.log_entries + self.scheduled_log_entries

    @staticmethod
    def filter_options() -> list[str]:
        return ['name', 'log #', 'scheduled logs', 'latest']

    def get_all_entry_logs(self) -> list[LogEntry | ScheduledLogEntry]:
        return self.log_entries + self.scheduled_log_entries

    def create_entry(self, entry_data: dict) -> str:
        """Creates a new entry adding it to the list and returns its unique id."""
        try:
            new_entry = LogEntry(desc=entry_data['desc'],
                                 date=entry_data['date'],
                                 mileage=entry_data['mileage'],
                                 category=EntryCategory(entry_data['category']),
                                 tags=entry_data['tags'],
                                 component=self,
                                 _id=str(uuid.uuid1()),
                                 custom_info=entry_data.get('custom_info') or {})

        except Exception:
            Printer.print_msg(None, 'ADD_FAIL', name="new entry", relation=self.name)
        else:
            self.log_entries.append(new_entry)

            Printer.print_msg(new_entry, 'ADD_SUCCESS', name=f"Entry of id '{new_entry.id}'", relation=self.name)

            self._update_current_part(new_entry)
            self._update_mileage(new_entry)

            return new_entry.id

    def create_entry_from_file(self, entry_data: dict) -> str:
        """Creates a new entry adding it to the list without creating new id."""

        new_entry = LogEntry(desc=entry_data['desc'],
                             date=entry_data['date'],
                             mileage=entry_data['mileage'],
                             category=EntryCategory(entry_data['category']),
                             tags=entry_data['tags'],
                             component=self,
                             _id=entry_data['id'],
                             custom_info=entry_data.get('custom_info') or {})
        self.log_entries.append(new_entry)

        self._update_current_part(new_entry)
        self._update_mileage(new_entry)

        return new_entry.id

    def create_scheduled_entry(self, entry_data: dict) -> str:
        """Creates a new scheduled entry adding it to the list and returns its unique id."""
        try:
            new_entry = ScheduledLogEntry(desc=entry_data['desc'],
                                          date=entry_data['date'],
                                          mileage=entry_data['mileage'],
                                          category=EntryCategory(entry_data['category']),
                                          tags=entry_data['tags'],
                                          component=self,
                                          _id=str(uuid.uuid1()),
                                          custom_info=entry_data.get('custom_info') or {},
                                          frequency=entry_data['frequency'],
                                          repeating=entry_data['repeating'])

            new_entry.rule = entry_data.get('rule', 'date')

            if entry_data['frequency'] <= 0 and entry_data['repeating'] is True:
                raise ValueError("Frequency of scheduled entry cannot be 0 if it's supposed to be repeating!")
        except Exception as e:
            Printer.print_msg(ScheduledLogEntry, 'ADD_FAIL', name="new scheduled entry", relation=self.name,
                              reason=f"reason={e}")
        else:
            Printer.print_msg(new_entry, 'ADD_SUCCESS',
                              name=f"Scheduled entry of id '{new_entry.id}'", relation=self.name)
            self.scheduled_log_entries.append(new_entry)

            return new_entry.id

    def create_scheduled_entry_from_file(self, entry_data: dict) -> str:
        """Creates a new scheduled entry adding it to the list and returns its unique id."""
        try:
            clamped_mil = self._clamp_scheduled_entry_mileage(entry_data)

            new_entry = ScheduledLogEntry(desc=entry_data['desc'],
                                          date=entry_data['date'],
                                          mileage=clamped_mil,
                                          category=EntryCategory(entry_data['category']),
                                          tags=entry_data['tags'],
                                          component=self,
                                          _id=entry_data['id'],
                                          custom_info=entry_data.get('custom_info') or {},
                                          frequency=entry_data['frequency'],
                                          repeating=entry_data['repeating'],
                                          _from_file=True)

            new_entry.rule = entry_data.get('rule', 'date')

            if entry_data['frequency'] <= 0 and entry_data['repeating'] is True:
                raise ValueError("Frequency of scheduled entry cannot be 0 if it's supposed to be repeating!")
        except Exception as e:
            Printer.print_msg(ScheduledLogEntry, 'ADD_FAIL', name="loaded scheduled entry", relation=self.name,
                              reason=f"reason={e}")
        else:
            self.scheduled_log_entries.append(new_entry)

            return new_entry.id

    def mark_scheduled_entry_as_done(self, entry_id: str):
        entry = self.get_entry_by_id(entry_id)
        entry.mileage = self.parent.car.mileage
        entry.date = TODAY
        new_entry_id = self.create_entry(entry.to_json())

        if not entry.repeating:
            self.delete_entry_by_id(entry_id)
        else:
            Printer.print_msg(ScheduledLogEntry,
                              'ADD_SUCCESS',
                              name=f"Entry '{entry.desc.strip()}' has been renewed for "
                                   f"{entry.get_new_date()} and",
                              relation=self.name)
            entry.repeat()

            new_entry = self.get_entry_by_id(new_entry_id)
            self._update_current_part(new_entry)
            self._update_mileage(new_entry)

            return entry

    def update_entry(self, entry_id: str, changes: dict):
        """Update values of log entry with specified unique id hash. \n
        'entry_changes' is a dictionary that contains only keys that are to be overwritten and their new values.\n
        Unique ID of updated entry cannot be changed."""

        entry_to_update = self.get_entry_by_id(entry_id)

        for k, v in changes.items():
            if k not in ("_id", "id"):
                entry_to_update.to_json()[k] = v

        self._update_mileage(entry_to_update)

    def delete_entry_by_id(self, entry_id: str):
        """Delete log entry given it's unique id hash."""
        entry_to_delete = self.get_entry_by_id(entry_id)

        if entry_to_delete:
            self.refresh_parts()

            match entry_to_delete.__class__.__name__:
                case 'LogEntry':
                    self.log_entries.remove(entry_to_delete)
                case 'ScheduledLogEntry':
                    self.scheduled_log_entries.remove(entry_to_delete)

            Printer.print_msg(entry_to_delete, 'DEL_SUCCESS',
                              name=f"Entry of id '{entry_to_delete.id}'", relation=self.name)
        else:
            Printer.print_msg(LogEntry, 'DEL_FAIL',
                              name=f"Entry of id '{entry_to_delete.id}'", relation=self.name)

    def delete_entry_by_index(self, entry_index: int = -1):
        """Removes log entry from list at target index, removes last one by default."""
        try:
            deleted_entry = self.log_entries.pop(entry_index)
            self.refresh_parts()
            Printer.print_msg(LogEntry, 'DEL_SUCCESS',
                              name=f"Entry of id '{deleted_entry.id}'", relation=self.name)
        except IndexError:
            Printer.print_msg(LogEntry, 'DEL_FAIL',
                              name=f"entry'",
                              relation=self.name, reason=f"as it was not found  at index {entry_index}")

    def delete_children(self, clear_parts=False):
        """Delete all entry logs."""
        self.log_entries.clear()
        self.scheduled_log_entries.clear()

        if clear_parts:
            self.current_part = None
            self.part_list = []

    def get_entry_by_id(self, entry_id: str) -> LogEntry | ScheduledLogEntry | None:
        """Return log entry by its unique id hash."""
        i = 0

        while i < len(self.log_entries):
            if self.log_entries[i].id == entry_id:
                return self.log_entries[i]
            else:
                i += 1

        i = 0

        while i < len(self.scheduled_log_entries):
            if self.scheduled_log_entries[i].id == entry_id:
                return self.scheduled_log_entries[i]
            else:
                i += 1

        Printer.print_msg(LogEntry, 'READ_FAIL', name=entry_id, relation=self.parent.name)

    def to_json(self) -> dict:
        """Returns object properties as JSON-serializable dictionary."""
        d = {'type': 'component',
             'name': self.name,
             'current_part': self._clamp_current_part(),
             'part_list': [part.to_json() for part in self.part_list],
             'desc': self.desc,
             'log_entries': [entry.to_json() for entry in self.log_entries],
             'scheduled_log_entries': [entry.to_json() for entry in self.scheduled_log_entries],
             'custom_info': self.custom_info,
             }

        return d

    def _clamp_current_part(self):
        if self.current_part:
            return self.current_part.to_json()
        else:
            return ''

    def refresh_parts(self):
        parts = []

        for entry in self.log_entries:
            keys = [k.lower() for k in entry.custom_info.keys()]
            try:
                part_id = keys.index('part')
                name = list(entry.custom_info.values())[part_id]
                parts.append(Part(name=name, parent_entry_id=entry.id, custom_info={}))
            except ValueError:
                pass

        self.part_list = parts

        if len(self.part_list) > 0:
            self.current_part = self.part_list[-1]
        else:
            self.current_part = ''

    def get_target_path(self, extension: str) -> str:
        """Extension without the dot"""
        if '.' in self.path.suffix:
            return self.path

        return self.path.joinpath(f"{self.parent.name}_{self.name.replace(' ', '_')}.{extension}")

    def get_formatted_info(self) -> str:
        """Return well-formatted string representing data of this class."""
        result = f"{self.name} ({len(self.log_entries)}): \n"

        for entry in self.log_entries:
            result += f"{entry.get_formatted_info()}"

        result += f"\nScheduled:\n"
        for entry in self.scheduled_log_entries:
            result += f"{entry.get_formatted_info()}\n"

        return result

    def add_part(self, part_info: dict):
        new_part = Part(**part_info)
        self.part_list.append(new_part)

    def _update_current_part(self, entry: LogEntry):
        if new_part := entry.custom_info.get('part'):

            if self.current_part != new_part:
                self.current_part = Part(new_part, entry.id)

                self.part_list.append(self.current_part)

    def _update_mileage(self, entry: LogEntry):
        new_mileage = entry.mileage

        if new_mileage > self.current_mileage:
            self.current_mileage = new_mileage

    def car_mileage_needs_update(self, entry: LogEntry) -> bool:
        if entry.mileage > self.parent.car.car_info.mileage:
            return True
        else:
            return False

    def _clamp_scheduled_entry_mileage(self, entry_data) -> int:
        if entry_data['rule'] == 'mileage':
            return entry_data['mileage']
        else:
            return self.current_mileage

    def __repr__(self) -> str:
        return f"[COMPONENT] {self.name} ({len(self.log_entries)} Entries)\n"
