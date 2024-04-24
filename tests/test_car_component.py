import pytest

from carlogger.items.car_component import CarComponent
from carlogger.const import TODAY
from carlogger.util import date_n_days_from_now


def test_log_entry_is_added_successfully(mock_log_entry):
    c = CarComponent("Coolant")
    c.create_entry(mock_log_entry)

    assert len(c.log_entries) > 0


def test_log_entry_is_removed_successfully(mock_log_entry):
    c = CarComponent("Coolant")
    entry_id = c.create_entry(mock_log_entry)
    c.delete_entry_by_id(entry_id)

    assert len(c.log_entries) < 1


def test_latest_mileage_is_updated_on_entry_add(mock_log_entry):
    c = CarComponent("Coolant")
    c.create_entry(mock_log_entry)

    assert c.current_mileage == mock_log_entry.get('mileage')


def test_log_entry_is_updated_successfully(mock_component):
    c = mock_component

    entry_id = c.log_entries[0].id
    entry_original = c.get_entry_by_id(entry_id)

    updated_entry = {"desc": "BellaCar Freeze G12 Coolant",
                     "date": (15, 3, 2019),
                     "mileage": 2000,
                     "category": "swap",
                     "tags": [],
                     }

    c.update_entry(entry_id, updated_entry)

    assert entry_original.desc == c.get_entry_by_id(entry_id).desc


def test_log_entry_updates_current_part(mock_component):
    c = mock_component
    new_part = "Motul 5w40 Extreme Sport"

    entry_data = {"desc": "New oil and oil filter. Note: get a better tool for removing oil filters.",
                  "date": (12, 8, 2023),
                  "mileage": 3455,
                  "category": "fluid_change",
                  "tags": [],
                  "custom_info":
                      {
                          "part": new_part
                      }
                  }

    c.create_entry(entry_data)

    assert c.current_part == new_part


def test_log_entry_does_not_update_current_part(mock_component):
    c = mock_component
    new_part = "Motul 5w40 Extreme Sport"

    entry_data = {"desc": "New oil and oil filter. Note: get a better tool for removing oil filters.",
                  "date": (12, 8, 2023),
                  "mileage": 3455,
                  "category": "fluid_add",
                  "tags": [],
                  "custom_info":
                      {
                          "part": new_part
                      }
                  }

    c.create_entry(entry_data)

    assert c.current_part != new_part


def test_scheduled_log_entry_is_added(mock_component, mock_log_entry):
    c = mock_component
    mock_component.create_scheduled_entry(mock_log_entry)

    assert len(c.log_entries) > 0


def test_scheduled_log_entry_returns_days_remaining(mock_component, mock_scheduled_log_entry):
    c = mock_component
    mock_component.create_scheduled_entry(mock_scheduled_log_entry)
    entry = c.scheduled_log_entries[0]

    assert entry.get_days_remaining() < 0


def test_scheduled_log_entry_returns_mileage_remaining(mock_component, mock_log_entry, mock_scheduled_log_entry):
    c = mock_component
    c = CarComponent("Coolant")
    c.create_entry(mock_log_entry)
    c.create_scheduled_entry(mock_scheduled_log_entry)

    entry = c.scheduled_log_entries[0]

    assert entry.get_mileage_remaining() == 976


def test_scheduled_log_entry_completion(mock_component, mock_log_entry, mock_scheduled_log_entry):
    c = mock_component
    c = CarComponent("Coolant")
    c.create_scheduled_entry(mock_scheduled_log_entry)

    entry = c.scheduled_log_entries[0].id

    c.mark_scheduled_entry_as_done(entry)

    assert len(c.log_entries) > 0


def test_scheduled_log_entry_completion_refreshes(mock_component, mock_log_entry, mock_scheduled_log_entry):
    c = mock_component
    c = CarComponent("Coolant")
    c.create_scheduled_entry(mock_scheduled_log_entry)

    entry = c.scheduled_log_entries[0]
    og_date = entry.date

    c.mark_scheduled_entry_as_done(entry.id)

    assert og_date != c.scheduled_log_entries[0].date


@pytest.mark.parametrize("entry_data, expected", [
    ({"desc": "Engine Checkup",
      "date": TODAY,
      "mileage": 2380,
      "category": 'swap',
      "tags": [],
      "repeating": True,
      "day_frequency": 10,
      },
     "in 10 days"),
    ({"desc": "Engine Checkup",
      "date": date_n_days_from_now(-20),
      "mileage": 2380,
      "category": 'swap',
      "tags": [],
      "repeating": True,
      "day_frequency": 10,
      },
     "10 days ago"),
    ({"desc": "Engine Checkup",
      "date": date_n_days_from_now(-10),
      "mileage": 2380,
      "category": 'swap',
      "tags": [],
      "repeating": True,
      "day_frequency": 10,
      },
     "")
])
def test_scheduled_log_entry_returns_days_remaining_string(mock_component, entry_data, expected):
    entry_id = mock_component.create_scheduled_entry(entry_data)
    entry = mock_component.get_entry_by_id(entry_id)

    assert entry.days_remaining_to_str() == expected
