import pytest


def test_create_collection(mock_car):
    car = mock_car
    car.create_collection('Engine')

    assert len(car.collections) == 1


def test_create_nested_collection(mock_car):
    car = mock_car
    car.create_collection('Engine')
    car.create_nested_collection('Turbocharger', 'Engine')

    assert len(car.collections) == 2


def test_delete_collection(mock_car):
    car = mock_car
    car.create_collection('Engine')
    car.delete_collection('Engine')

    assert len(car.collections) == 0


def test_raises_on_duplicate_collection(mock_car):
    with pytest.raises(ValueError):
        car = mock_car
        car.create_collection('Engine')
        car.create_collection('Engine')


def test_raises_on_collection_not_found(mock_car):
    with pytest.raises(ValueError):
        mock_car.get_collection_by_name('Test')


def test_raises_on_component_not_found(mock_car):
    with pytest.raises(ValueError):
        mock_car.get_component_by_name('Test')
