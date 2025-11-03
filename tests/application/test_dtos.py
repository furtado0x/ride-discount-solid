"""Tests for application DTOs."""

from datetime import datetime
from decimal import Decimal

import pytest

from ride_discount.application.dtos import RideContext


class TestRideContext:
    """Tests for RideContext DTO."""

    def test_create_ride_context_with_valid_data(self, customer_no_rides, base_price):
        """Test creating a ride context with valid data."""
        ride_datetime = datetime(2024, 1, 10, 14, 30)
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("10"),
            base_price=base_price,
            ride_datetime=ride_datetime,
        )
        assert context.customer == customer_no_rides
        assert context.distance_km == Decimal("10")
        assert context.base_price == base_price
        assert context.ride_datetime == ride_datetime

    def test_ride_context_is_immutable(self, customer_no_rides, base_price):
        """Test that ride context is immutable (frozen)."""
        ride_datetime = datetime(2024, 1, 10, 14, 30)
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("10"),
            base_price=base_price,
            ride_datetime=ride_datetime,
        )
        with pytest.raises(AttributeError):
            context.distance_km = Decimal("20")  # type: ignore

    def test_ride_context_with_negative_distance_raises_error(
        self, customer_no_rides, base_price
    ):
        """Test that negative distance raises ValueError."""
        ride_datetime = datetime(2024, 1, 10, 14, 30)
        with pytest.raises(ValueError, match="distance_km must be non-negative"):
            RideContext(
                customer=customer_no_rides,
                distance_km=Decimal("-1"),
                base_price=base_price,
                ride_datetime=ride_datetime,
            )

    def test_ride_context_with_negative_price_raises_error(
        self, customer_no_rides
    ):
        """Test that negative base price raises ValueError."""
        ride_datetime = datetime(2024, 1, 10, 14, 30)
        with pytest.raises(ValueError, match="base_price must be non-negative"):
            RideContext(
                customer=customer_no_rides,
                distance_km=Decimal("10"),
                base_price=Decimal("-10"),
                ride_datetime=ride_datetime,
            )

    def test_ride_context_with_zero_values(self, customer_no_rides):
        """Test creating ride context with zero distance and price."""
        ride_datetime = datetime(2024, 1, 10, 14, 30)
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("0"),
            base_price=Decimal("0"),
            ride_datetime=ride_datetime,
        )
        assert context.distance_km == Decimal("0")
        assert context.base_price == Decimal("0")
