"""Shared fixtures for pytest tests."""

from datetime import datetime
from decimal import Decimal

import pytest

from ride_discount.application.dtos import RideContext
from ride_discount.domain.entities import Customer


@pytest.fixture
def customer_no_rides() -> Customer:
    """Customer with no completed rides."""
    return Customer(id="CUST-001", total_rides=0)


@pytest.fixture
def customer_few_rides() -> Customer:
    """Customer with few completed rides (25)."""
    return Customer(id="CUST-002", total_rides=25)


@pytest.fixture
def customer_many_rides() -> Customer:
    """Customer with many completed rides (75)."""
    return Customer(id="CUST-003", total_rides=75)


@pytest.fixture
def customer_max_frequency_discount() -> Customer:
    """Customer with enough rides for maximum frequency discount (150 rides)."""
    return Customer(id="CUST-004", total_rides=150)


@pytest.fixture
def weekday_midday() -> datetime:
    """Datetime representing a weekday at midday (Wednesday 14:30)."""
    return datetime(2024, 1, 10, 14, 30)  # Wednesday


@pytest.fixture
def weekday_rush_hour() -> datetime:
    """Datetime representing a weekday rush hour (Wednesday 8:00)."""
    return datetime(2024, 1, 10, 8, 0)  # Wednesday


@pytest.fixture
def late_night() -> datetime:
    """Datetime representing late night hours (3:00 AM)."""
    return datetime(2024, 1, 10, 3, 0)


@pytest.fixture
def weekend_midday() -> datetime:
    """Datetime representing a weekend midday (Saturday 14:30)."""
    return datetime(2024, 1, 13, 14, 30)  # Saturday


@pytest.fixture
def base_price() -> Decimal:
    """Standard base price for rides."""
    return Decimal("100.00")


@pytest.fixture
def short_distance() -> Decimal:
    """Short distance ride (3km)."""
    return Decimal("3")


@pytest.fixture
def medium_distance() -> Decimal:
    """Medium distance ride (10km)."""
    return Decimal("10")


@pytest.fixture
def long_distance() -> Decimal:
    """Long distance ride (25km)."""
    return Decimal("25")


@pytest.fixture
def ride_context_basic(
    customer_no_rides: Customer,
    short_distance: Decimal,
    base_price: Decimal,
    weekday_rush_hour: datetime,
) -> RideContext:
    """Basic ride context with no discounts expected."""
    return RideContext(
        customer=customer_no_rides,
        distance_km=short_distance,
        base_price=base_price,
        ride_datetime=weekday_rush_hour,
    )


@pytest.fixture
def ride_context_multiple_discounts(
    customer_many_rides: Customer,
    long_distance: Decimal,
    base_price: Decimal,
    weekday_midday: datetime,
) -> RideContext:
    """Ride context that should trigger multiple discounts."""
    return RideContext(
        customer=customer_many_rides,
        distance_km=long_distance,
        base_price=base_price,
        ride_datetime=weekday_midday,
    )
