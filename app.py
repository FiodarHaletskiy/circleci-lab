"""Модуль расчёта стоимости и сроков доставки посылок."""

import re

BASE_PRICE = 3.0  # базовый тариф, BYN
PRICE_PER_KG = 0.8  # BYN за килограмм
PRICE_PER_KM = 0.02  # BYN за километр
EXPRESS_FACTOR = 1.2  # наценка за экспресс-доставку
MAX_WEIGHT_KG = 30
KM_PER_DAY = 300
TRACKING_PATTERN = re.compile(r"^SHP-\d{6}$")


def calculate_shipping_cost(weight_kg, distance_km, express=False):
    """Возвращает стоимость доставки в BYN с точностью до копеек."""
    if weight_kg <= 0 or weight_kg > MAX_WEIGHT_KG:
        raise ValueError(f"Вес должен быть больше 0 и не больше {MAX_WEIGHT_KG} кг")
    if distance_km < 0:
        raise ValueError("Расстояние не может быть отрицательным")
    cost = BASE_PRICE + weight_kg * PRICE_PER_KG + distance_km * PRICE_PER_KM
    if express:
        cost *= EXPRESS_FACTOR
    return round(cost, 2)


def estimate_delivery_days(distance_km, express=False):
    """Возвращает срок доставки в днях: 1 день + 1 день на каждые 300 км."""
    if distance_km < 0:
        raise ValueError("Расстояние не может быть отрицательным")
    days = 1 + int(distance_km // KM_PER_DAY)
    if express:
        days = max(1, (days + 1) // 2)
    return days


def is_valid_tracking_number(value):
    """Проверяет формат трек-номера: SHP- и шесть цифр."""
    return isinstance(value, str) and bool(TRACKING_PATTERN.match(value))
