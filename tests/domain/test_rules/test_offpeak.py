"""Tests for off-peak hours discount rule."""

from datetime import datetime
from decimal import Decimal

import pytest

from ride_discount.application.dtos import RideContext
from ride_discount.domain.rules.offpeak import OffPeakDiscountRule


class TestOffPeakDiscountRule:
    """Tests for OffPeakDiscountRule."""

    @pytest.fixture
    def rule(self):
        """Create an off-peak discount rule instance."""
        return OffPeakDiscountRule()

    @pytest.mark.parametrize(
        "hour,expected_discount,expected_reason",
        [
            (0, Decimal("20"), "Late night off-peak discount"),
            (1, Decimal("20"), "Late night off-peak discount"),
            (3, Decimal("20"), "Late night off-peak discount"),
            (5, Decimal("20"), "Late night off-peak discount"),
        ],
    )
    def test_late_night_discount(
        self, rule, hour, expected_discount, expected_reason, customer_no_rides, base_price
    ):
        """Test late night discount (0-6h) applies correctly."""
        ride_time = datetime(2024, 1, 10, hour, 0)  # Wednesday
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=ride_time,
        )
        result = rule.calculate_discount(context)
        assert result is not None
        assert result.discount_percentage == expected_discount
        assert result.reason == expected_reason

    @pytest.mark.parametrize("hour", [10, 11, 12, 13, 14, 15])
    def test_midday_weekday_discount(self, rule, hour, customer_no_rides, base_price):
        """Test mid-day weekday discount (10-16h Monday-Friday) applies correctly."""
        ride_time = datetime(2024, 1, 10, hour, 0)  # Wednesday
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=ride_time,
        )
        result = rule.calculate_discount(context)
        assert result is not None
        assert result.discount_percentage == Decimal("10")
        assert result.reason == "Mid-day off-peak discount"

    @pytest.mark.parametrize("hour", [10, 11, 12, 13, 14, 15])
    def test_no_midday_discount_on_weekend(self, rule, hour, customer_no_rides, base_price):
        """Test that mid-day discount does not apply on weekends."""
        ride_time = datetime(2024, 1, 13, hour, 0)  # Saturday
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=ride_time,
        )
        result = rule.calculate_discount(context)
        assert result is None

    @pytest.mark.parametrize("hour", [6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22, 23])
    def test_no_discount_during_rush_hours(self, rule, hour, customer_no_rides, base_price):
        """Test that no discount applies during rush hours."""
        ride_time = datetime(2024, 1, 10, hour, 0)  # Wednesday
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=ride_time,
        )
        result = rule.calculate_discount(context)
        assert result is None

    @pytest.mark.parametrize(
        "weekday,hour,should_have_discount",
        [
            (0, 14, True),   # Monday midday
            (1, 14, True),   # Tuesday midday
            (2, 14, True),   # Wednesday midday
            (3, 14, True),   # Thursday midday
            (4, 14, True),   # Friday midday
            (5, 14, False),  # Saturday midday
            (6, 14, False),  # Sunday midday
        ],
    )
    def test_midday_discount_by_weekday(
        self, rule, weekday, hour, should_have_discount, customer_no_rides, base_price
    ):
        """Test mid-day discount applies only on weekdays."""
        # 2024-01-08 is Monday (weekday 0)
        ride_time = datetime(2024, 1, 8 + weekday, hour, 0)
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=ride_time,
        )
        result = rule.calculate_discount(context)
        if should_have_discount:
            assert result is not None
            assert result.discount_percentage == Decimal("10")
        else:
            assert result is None

    def test_boundary_hour_6_no_late_night_discount(
        self, rule, customer_no_rides, base_price
    ):
        """Test that hour 6 does not get late night discount."""
        ride_time = datetime(2024, 1, 10, 6, 0)  # 6:00 AM
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=ride_time,
        )
        result = rule.calculate_discount(context)
        assert result is None

    def test_boundary_hour_16_no_midday_discount(
        self, rule, customer_no_rides, base_price
    ):
        """Test that hour 16 does not get mid-day discount."""
        ride_time = datetime(2024, 1, 10, 16, 0)  # 4:00 PM Wednesday
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=ride_time,
        )
        result = rule.calculate_discount(context)
        assert result is None
