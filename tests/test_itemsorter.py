from carlogger.items.car import Car
from carlogger.items.item_sorter import ItemSorter
from carlogger.items.car_info import CarInfo


def test_cars_are_sorted_by_attribute(mock_car_dict_list):
    car_infos = [CarInfo(**car) for car in mock_car_dict_list]
    item_sorter = ItemSorter(car_infos, 'mileage')
    sorted_items = item_sorter.get_sorted_list()

    assert sorted_items == [car_infos[0], car_infos[1]]


def test_cars_are_sorted_by_attribute_in_reverse(mock_car_dict_list):
    car_infos = [CarInfo(**car) for car in mock_car_dict_list]
    item_sorter = ItemSorter(car_infos, 'mileage')
    sorted_items = item_sorter.get_sorted_list(reverse_order=True)

    assert sorted_items == [car_infos[1], car_infos[0]]


def test_items_are_sorted_by_latest_entry(mock_car_full, mock_entry_dict_list):
    mock_cars_full = [mock_car_full, mock_car_full]
    mock_cars_full[1].collections[0].components[0].create_entry(mock_entry_dict_list)
    item_sorter = ItemSorter(mock_cars_full, 'latest')
    sorted_items = item_sorter.get_sorted_list(reverse_order=True)

    assert sorted_items == [mock_cars_full[1], mock_cars_full[0]]


def test_items_are_sorted_by_oldest_entry(mock_cars_full):
    item_sorter = ItemSorter(mock_cars_full, 'oldest')
    sorted_items = item_sorter.get_sorted_list(reverse_order=True)

    assert sorted_items == [mock_cars_full[0], mock_cars_full[1]]


def test_entries_are_sorted_by_latest_entry(mock_car, mock_entry_dict_list):
    coll = mock_car.create_collection('TestColl')
    comp = coll.create_component('TestComp')
    [comp.create_entry(entry) for entry in mock_entry_dict_list]
    entries = comp.log_entries

    item_sorter = ItemSorter(entries, 'latest')
    sorted_items = item_sorter.get_sorted_list(reverse_order=True)

    assert sorted_items == [entries[1], entries[0]]


def test_entries_are_sorted_by_oldest_entry(mock_car, mock_entry_dict_list):
    coll = mock_car.create_collection('TestColl')
    comp = coll.create_component('TestComp')
    [comp.create_entry(entry) for entry in mock_entry_dict_list]
    entries = comp.log_entries

    item_sorter = ItemSorter(entries, 'oldest')
    sorted_items = item_sorter.get_sorted_list(reverse_order=True)

    assert sorted_items == [entries[0], entries[1]]


def test_returns_valid_sort_method(mock_car_dict_list):
    car_infos = [CarInfo(**car) for car in mock_car_dict_list]
    cars = [Car(car_info) for car_info in car_infos]
    item_sorter = ItemSorter(cars, sort_method='latest')

    assert item_sorter._get_sort_method() == item_sorter.sort_by_latest_entry
