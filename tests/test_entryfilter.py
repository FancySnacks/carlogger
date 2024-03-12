import pytest

from carlogger.entryfilter import EntryFilter


def test_count_filter_is_created():
    entryfilter = EntryFilter()
    entryfilter.apply_filters_to_entry_list(['-5'], [])

    assert entryfilter.count_filter is not None


def test_filters_are_created():
    entryfilter = EntryFilter()
    entryfilter.apply_filters_to_entry_list(['<19-05-2001', '2'], [])

    assert len(entryfilter.filters) > 0


def test_filters_are_applied_to_entry_list(mock_log_entry, mock_component):
    entries = [mock_component.log_entries[0]]
    entryfilter = EntryFilter()
    filtered_entries = entryfilter.apply_filters_to_entry_list(['test', '2'], entries)

    assert entries[0] not in filtered_entries


@pytest.mark.parametrize("args, expected",
                         [(['*'], 'all'),
                          (['testetst'], 'desc'),
                          (['01-01-1999'], 'date'),
                          (['<12500'], 'mileage'),
                          (['>12500'], 'mileage'),
                          ])
def test_correct_filters_are_created(args, expected):
    entryfilter = EntryFilter()
    entryfilter._create_filter_group_from_args(args)

    assert entryfilter.filters[0].filter_group == expected
