from carlogger.items.car_component import CarComponent


def test_log_entry_is_added_successfully(mock_log_entry):
    c = CarComponent("Coolant")
    c.create_entry(mock_log_entry)

    assert len(c.log_entries) > 0


def test_log_entry_is_removed_successfully(mock_log_entry):
    c = CarComponent("Coolant")
    entry_id = c.create_entry(mock_log_entry)
    c.delete_entry_by_id(entry_id)

    assert len(c.log_entries) < 1


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

    assert entry.get_days_remaining() > 0
