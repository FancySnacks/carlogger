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
