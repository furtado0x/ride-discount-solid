"""Tests for ride frequency discount rule."""

from decimal import Decimal

import pytest

from ride_discount.application.dtos import RideContext
from ride_discount.domain.entities import Customer
from ride_discount.domain.rules.frequency import RideFrequencyDiscountRule


class TestRideFrequencyDiscountRule:
    """Tests for RideFrequencyDiscountRule."""

    @pytest.fixture
    def rule(self):
        """Create a frequency discount rule instance."""
        return RideFrequencyDiscountRule()

    def test_no_discount_for_zero_rides(self, rule, ride_context_basic):
        """Test that no discount is given for customers with zero rides."""
        result = rule.calculate_discount(ride_context_basic)
        assert result is None

    def test_no_discount_for_less_than_10_rides(self, rule, base_price, weekday_rush_hour):
        """Test that no discount is given for customers with less than 10 rides."""
        customer = Customer(id="CUST-001", total_rides=9)
        context = RideContext(
            customer=customer,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=weekday_rush_hour,
        )
        result = rule.calculate_discount(context)
        assert result is None

    @pytest.mark.parametrize(
        "total_rides,expected_discount",
        [
            (10, Decimal("1")),
            (20, Decimal("2")),
            (50, Decimal("5")),
            (75, Decimal("7")),
            (100, Decimal("10")),
            (150, Decimal("15")),
            (200, Decimal("15")),  # Capped at 15%
            (1000, Decimal("15")),  # Capped at 15%
        ],
    )
    def test_frequency_discount_calculation(
        self, rule, total_rides, expected_discount, base_price, weekday_rush_hour
    ):
        """Test frequency discount calculation for various ride counts."""
        customer = Customer(id="CUST-001", total_rides=total_rides)
        context = RideContext(
            customer=customer,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=weekday_rush_hour,
        )
        result = rule.calculate_discount(context)
        assert result is not None
        assert result.discount_percentage == expected_discount
        assert f"{total_rides} rides" in result.reason

    def test_discount_reason_format(self, rule, customer_many_rides, base_price, weekday_rush_hour):
        """Test that discount reason includes ride count."""
        context = RideContext(
            customer=customer_many_rides,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=weekday_rush_hour,
        )
        result = rule.calculate_discount(context)
        assert result is not None
        assert "Ride frequency discount" in result.reason
        assert "75 rides" in result.reason
