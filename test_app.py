import pytest

from app import (
    calculate_shipping_cost,
    estimate_delivery_days,
    is_valid_tracking_number,
)


@pytest.mark.parametrize(
    "weight, distance, expected",
    [
        (2, 100, 6.6),
        (10, 193.3, 14.87),
        (30, 0, 27.0),
    ],
)
def test_regular_cost(weight, distance, expected):
    assert calculate_shipping_cost(weight, distance) == pytest.approx(expected)


def test_express_cost_is_one_and_a_half_times_higher():
    assert calculate_shipping_cost(2, 100, express=True) == pytest.approx(9.9)


@pytest.mark.parametrize("weight", [0, -1, 31])
def test_invalid_weight_raises_error(weight):
    with pytest.raises(ValueError):
        calculate_shipping_cost(weight, 100)


def test_negative_distance_raises_error():
    with pytest.raises(ValueError):
        calculate_shipping_cost(5, -10)


@pytest.mark.parametrize(
    "distance, expected_days",
    [(0, 1), (299, 1), (300, 2), (650, 3)],
)
def test_delivery_days(distance, expected_days):
    assert estimate_delivery_days(distance) == expected_days


@pytest.mark.parametrize(
    "distance, expected_days",
    [(100, 1), (650, 2)],
)
def test_express_delivery_days(distance, expected_days):
    assert estimate_delivery_days(distance, express=True) == expected_days


def test_delivery_days_negative_distance_raises_error():
    with pytest.raises(ValueError):
        estimate_delivery_days(-1)


@pytest.mark.parametrize("number", ["SHP-100002", "SHP-000001"])
def test_valid_tracking_number(number):
    assert is_valid_tracking_number(number)


@pytest.mark.parametrize("number", ["SHP-12", "shp-100002", "", None, 100002])
def test_invalid_tracking_number(number):
    assert not is_valid_tracking_number(number)
