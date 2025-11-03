"""Tests for distance-based discount rule."""

from decimal import Decimal

import pytest

from ride_discount.application.dtos import RideContext
from ride_discount.domain.rules.distance import ProportionalDistanceDiscountRule


class TestProportionalDistanceDiscountRule:
    """Tests for ProportionalDistanceDiscountRule."""

    @pytest.fixture
    def rule(self):
        """Create a distance discount rule instance."""
        return ProportionalDistanceDiscountRule()

    def test_no_discount_for_5km_or_less(self, rule, customer_no_rides, base_price, weekday_rush_hour):
        """Test that no discount is given for rides of 5km or less."""
        for distance in [Decimal("1"), Decimal("3"), Decimal("5")]:
            context = RideContext(
                customer=customer_no_rides,
                distance_km=distance,
                base_price=base_price,
                ride_datetime=weekday_rush_hour,
            )
            result = rule.calculate_discount(context)
            assert result is None

    @pytest.mark.parametrize(
        "distance,expected_discount",
        [
            (Decimal("6"), Decimal("0.5")),   # 1km over = 0.5%
            (Decimal("7"), Decimal("1.0")),   # 2km over = 1.0%
            (Decimal("10"), Decimal("2.5")),  # 5km over = 2.5%
            (Decimal("15"), Decimal("5.0")),  # 10km over = 5.0%
            (Decimal("25"), Decimal("10.0")), # 20km over = 10.0%
            (Decimal("45"), Decimal("20.0")), # 40km over = 20.0% (capped)
            (Decimal("100"), Decimal("20.0")),# 95km over = 20.0% (capped)
        ],
    )
    def test_distance_discount_calculation(
        self, rule, distance, expected_discount, customer_no_rides, base_price, weekday_rush_hour
    ):
        """Test distance discount calculation for various distances."""
        context = RideContext(
            customer=customer_no_rides,
            distance_km=distance,
            base_price=base_price,
            ride_datetime=weekday_rush_hour,
        )
        result = rule.calculate_discount(context)
        assert result is not None
        assert result.discount_percentage == expected_discount
        assert f"{distance}km" in result.reason

    def test_discount_reason_format(self, rule, customer_no_rides, base_price, weekday_rush_hour):
        """Test that discount reason includes distance."""
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("25"),
            base_price=base_price,
            ride_datetime=weekday_rush_hour,
        )
        result = rule.calculate_discount(context)
        assert result is not None
        assert "Distance discount" in result.reason
        assert "25km" in result.reason

    def test_boundary_conditions(self, rule, customer_no_rides, base_price, weekday_rush_hour):
        """Test boundary conditions for distance discount."""
        # Exactly 5km - no discount
        context_5km = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("5"),
            base_price=base_price,
            ride_datetime=weekday_rush_hour,
        )
        assert rule.calculate_discount(context_5km) is None

        # Just over 5km - minimal discount
        context_5_1km = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("5.1"),
            base_price=base_price,
            ride_datetime=weekday_rush_hour,
        )
        result = rule.calculate_discount(context_5_1km)
        assert result is not None
        assert result.discount_percentage == Decimal("0.05")  # 0.1 * 0.5
