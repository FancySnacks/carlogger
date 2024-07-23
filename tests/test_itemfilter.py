import pytest

from carlogger.items.item_filter import ItemFilter


itemfilter = ItemFilter()


@pytest.mark.parametrize('filters,expected',
                         [(["date<25-07-2024"], 1),
                          (["date=09-03-1964"], 1),
                          (["date=09-03-1964 09-03-1964"], 1),
                          ])
def test_filter_list_of_entries_by_date(mock_log_entry, mock_component, filters, expected):
    items = itemfilter.filter_items(mock_component.log_entries, filters)
    assert len(items) == expected


@pytest.mark.parametrize('filters,expected',
                         [(["mileage=1404"], 1),
                          (["mileage>1400"], 1),
                          (["mileage<1500"], 1),
                          (["mileage=>1400"], 1),
                          (["mileage<=1500"], 1)])
def test_filter_list_of_entries_by_mileage(mock_log_entry, mock_component, filters, expected):
    items = itemfilter.filter_items(mock_component.log_entries, filters)
    assert len(items) == expected


def test_filter_entries_by_id(mock_log_entry, mock_component):
    entry_id = mock_component.create_entry(mock_log_entry)
    items = itemfilter.filter_items(mock_component.log_entries, [f"id={entry_id}"])
    assert len(items) == 1
