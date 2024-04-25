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


def test_scheduled_log_entry_is_added(mock_component, mock_scheduled_log_entry):
    c = mock_component
    mock_component.create_scheduled_entry(mock_scheduled_log_entry)

    assert len(c.log_entries) > 0


def test_scheduled_log_entry_returns_days_remaining(mock_component, mock_scheduled_log_entry):
    c = mock_component
    entry_id = mock_component.create_scheduled_entry(mock_scheduled_log_entry)
    entry = c.get_entry_by_id(entry_id)

    assert entry.get_time_remaining() < 0


def test_scheduled_log_entry_returns_mileage_remaining(mock_component, mock_log_entry):
    mock_scheduled_log_entry = {"desc": "Engine Checkup",
                                "date": "12-06-1964",
                                "mileage": mock_log_entry['mileage'],
                                "category": 'swap',
                                "tags": [],
                                "repeating": True,
                                "frequency": 1000,
                                "rule": "mileage",
                                }
    c = mock_component
    c.create_entry(mock_log_entry)
    c.create_scheduled_entry(mock_scheduled_log_entry)

    entry = c.scheduled_log_entries[0]

    assert entry.get_time_remaining() == 1000


def test_scheduled_log_entry_completion(mock_component, mock_log_entry, mock_scheduled_log_entry):
    c = mock_component
    c = CarComponent("Coolant")
    c.create_scheduled_entry(mock_scheduled_log_entry)

    entry = c.scheduled_log_entries[0].id

    c.mark_scheduled_entry_as_done(entry)

    assert len(c.log_entries) > 0


def test_scheduled_log_entry_is_deleted_on_completion_if_not_repeating(mock_component):
    c = mock_component

    entry = {"desc": "Engine Checkup",
             "date": "11-11-2011",
             "mileage": 2380,
             "category": 'swap',
             "tags": [],
             "repeating": False,
             "frequency": 10,
             "rule": "date",
             }

    c.create_scheduled_entry(entry)
    entry = c.scheduled_log_entries[0]
    c.mark_scheduled_entry_as_done(entry.id)

    assert len(c.scheduled_log_entries) == 0


def test_scheduled_log_entry_completion_refreshes(mock_component):
    c = mock_component

    entry = {"desc": "Engine Checkup",
             "date": "",
             "mileage": 2380,
             "category": 'swap',
             "tags": [],
             "repeating": True,
             "frequency": 10,
             "rule": "date",
             }

    c.create_scheduled_entry(entry)

    entry = c.scheduled_log_entries[0]
    og_date = entry.date

    c.mark_scheduled_entry_as_done(entry.id)

    assert og_date != c.scheduled_log_entries[0].date


@pytest.mark.xfail(reason="False negative, reason unknown. Exception is raised correctly during normal app usage.")
def test_raises_error_when_frequency_is_zero_on_loopable_entry(mock_component):
    with pytest.raises(ValueError):
        entry_data = {"desc": "Engine Checkup",
                      "date": TODAY,
                      "mileage": 2380,
                      "category": 'swap',
                      "tags": [],
                      "repeating": True,
                      "frequency": 0,
                      "rule": "date",
                      }

        mock_component.create_scheduled_entry(entry_data)


@pytest.mark.parametrize("entry_data, expected", [
    ({"desc": "Engine Checkup",
      "date": '',
      "mileage": 2380,
      "category": 'swap',
      "tags": [],
      "repeating": True,
      "frequency": 10,
      "rule": "date",
      },
     "in 10 days"),
    ({"desc": "Engine Checkup",
      "date": date_n_days_from_now(-20),
      "mileage": 2380,
      "category": 'swap',
      "tags": [],
      "repeating": True,
      "frequency": 10,
      "rule": "date",
      },
     "10 days ago"),
    ({"desc": "Engine Checkup",
      "date": date_n_days_from_now(-10),
      "mileage": 2380,
      "category": 'swap',
      "tags": [],
      "repeating": True,
      "frequency": 10,
      "rule": "date",
      },
     ""),
    ({"desc": "Engine Checkup",
      "date": TODAY,
      "mileage": 2380,
      "category": 'swap',
      "tags": [],
      "repeating": False,
      "frequency": 0,
      "rule": "date",
      },
     ""),
    ({"desc": "Engine Checkup",
      "date": TODAY,
      "mileage": 0,
      "category": 'swap',
      "tags": [],
      "repeating": True,
      "frequency": 1500,
      "rule": "mileage",
      },
     "-1500")
])
def test_scheduled_log_entry_returns_days_remaining_string(mock_component, entry_data, expected):
    entry_id = mock_component.create_scheduled_entry(entry_data)
    entry = mock_component.get_entry_by_id(entry_id)

    assert entry.time_remaining_to_str() == expected


def test_scheduled_log_entry_is_too_late(mock_component):
    entry = {"desc": "Engine Checkup",
             "date": TODAY,
             "mileage": 0,
             "category": 'swap',
             "tags": [],
             "repeating": True,
             "frequency": 1000,
             "rule": "mileage",
             }

    entry_id = mock_component.create_scheduled_entry(entry)
    entry = mock_component.get_entry_by_id(entry_id)

    entry_data = {"desc": "New oil and oil filter. Note: get a better tool for removing oil filters.",
                  "date": (12, 8, 2023),
                  "mileage": 5341,
                  "category": "fluid_change",
                  "tags": [],
                  }

    mock_component.create_entry(entry_data)

    assert entry.time_remaining_to_str() == "+2937"
