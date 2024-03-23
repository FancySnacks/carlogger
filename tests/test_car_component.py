from carlogger.car_component import CarComponent


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
