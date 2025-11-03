"""Tests for calculate ride discount use case."""

from datetime import datetime
from decimal import Decimal

import pytest

from ride_discount.application.dtos import RideContext
from ride_discount.application.use_cases import CalculateRideDiscountUseCase
from ride_discount.domain.entities import Customer


class TestCalculateRideDiscountUseCase:
    """Tests for CalculateRideDiscountUseCase."""

    @pytest.fixture
    def use_case(self):
        """Create a use case instance."""
        return CalculateRideDiscountUseCase()

    def test_no_discounts_applied(self, use_case, ride_context_basic):
        """Test calculation when no discounts apply."""
        final_price, applied_discounts = use_case.execute(ride_context_basic)

        assert final_price == ride_context_basic.base_price
        assert len(applied_discounts) == 0

    def test_single_frequency_discount(self, use_case, base_price):
        """Test calculation with only frequency discount."""
        customer = Customer(id="CUST-001", total_rides=50)  # 5% discount
        context = RideContext(
            customer=customer,
            distance_km=Decimal("3"),  # No distance discount
            base_price=base_price,
            ride_datetime=datetime(2024, 1, 10, 8, 0),  # No off-peak discount
        )

        final_price, applied_discounts = use_case.execute(context)

        assert len(applied_discounts) == 1
        assert applied_discounts[0].discount_percentage == Decimal("5")
        assert "frequency" in applied_discounts[0].reason.lower()
        assert final_price == Decimal("95.00")  # 100 - 5%

    def test_single_distance_discount(self, use_case, customer_no_rides, base_price):
        """Test calculation with only distance discount."""
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("15"),  # 5% discount (10km over 5km * 0.5)
            base_price=base_price,
            ride_datetime=datetime(2024, 1, 10, 8, 0),  # No off-peak discount
        )

        final_price, applied_discounts = use_case.execute(context)

        assert len(applied_discounts) == 1
        assert applied_discounts[0].discount_percentage == Decimal("5.0")
        assert "distance" in applied_discounts[0].reason.lower()
        assert final_price == Decimal("95.00")  # 100 - 5%

    def test_single_offpeak_discount(self, use_case, customer_no_rides, base_price):
        """Test calculation with only off-peak discount."""
        context = RideContext(
            customer=customer_no_rides,
            distance_km=Decimal("3"),  # No distance discount
            base_price=base_price,
            ride_datetime=datetime(2024, 1, 10, 3, 0),  # Late night: 20% discount
        )

        final_price, applied_discounts = use_case.execute(context)

        assert len(applied_discounts) == 1
        assert applied_discounts[0].discount_percentage == Decimal("20")
        assert "late night" in applied_discounts[0].reason.lower()
        assert final_price == Decimal("80.00")  # 100 - 20%

    def test_multiple_discounts_applied(self, use_case, ride_context_multiple_discounts):
        """Test calculation with multiple discounts."""
        final_price, applied_discounts = use_case.execute(ride_context_multiple_discounts)

        # Should have 3 discounts: frequency (7%), distance (10%), off-peak (10%)
        assert len(applied_discounts) == 3

        total_discount = sum(d.discount_percentage for d in applied_discounts)
        assert total_discount == Decimal("27")  # 7 + 10 + 10

        # 100 - 27% = 73.00
        assert final_price == Decimal("73.00")

    def test_discount_cap_at_50_percent(self, use_case, base_price):
        """Test that total discount is capped at 50%."""
        # Create scenario with discounts totaling more than 50%
        customer = Customer(id="CUST-001", total_rides=200)  # 15% (capped)
        context = RideContext(
            customer=customer,
            distance_km=Decimal("100"),  # 20% (capped)
            base_price=base_price,
            ride_datetime=datetime(2024, 1, 10, 3, 0),  # 20% (late night)
        )
        # Total would be 55%, but should be capped at 50%

        final_price, applied_discounts = use_case.execute(context)

        assert len(applied_discounts) == 3
        total_discount = sum(d.discount_percentage for d in applied_discounts)
        assert total_discount == Decimal("55")  # Before cap

        # But final price should reflect 50% cap
        assert final_price == Decimal("50.00")  # 100 - 50%

    @pytest.mark.parametrize(
        "total_rides,distance,hour,expected_discount_count,expected_min_total",
        [
            (0, Decimal("3"), 8, 0, Decimal("0")),        # No discounts
            (50, Decimal("3"), 8, 1, Decimal("5")),       # Only frequency
            (0, Decimal("15"), 8, 1, Decimal("5")),       # Only distance
            (0, Decimal("3"), 3, 1, Decimal("20")),       # Only off-peak
            (50, Decimal("15"), 3, 3, Decimal("30")),     # All three
            (100, Decimal("25"), 14, 3, Decimal("30")),   # All three (weekday midday)
        ],
    )
    def test_various_discount_combinations(
        self,
        use_case,
        total_rides,
        distance,
        hour,
        expected_discount_count,
        expected_min_total,
        base_price,
    ):
        """Test various combinations of discount scenarios."""
        customer = Customer(id="CUST-001", total_rides=total_rides)
        context = RideContext(
            customer=customer,
            distance_km=distance,
            base_price=base_price,
            ride_datetime=datetime(2024, 1, 10, hour, 0),  # Wednesday
        )

        final_price, applied_discounts = use_case.execute(context)

        assert len(applied_discounts) == expected_discount_count
        if expected_discount_count > 0:
            total_discount = sum(d.discount_percentage for d in applied_discounts)
            assert total_discount >= expected_min_total
            assert final_price < base_price

    def test_zero_base_price(self, use_case, customer_many_rides):
        """Test calculation with zero base price."""
        context = RideContext(
            customer=customer_many_rides,
            distance_km=Decimal("25"),
            base_price=Decimal("0"),
            ride_datetime=datetime(2024, 1, 10, 14, 0),
        )

        final_price, applied_discounts = use_case.execute(context)

        # Should still calculate discounts, but final price is 0
        assert len(applied_discounts) > 0
        assert final_price == Decimal("0")

    def test_high_base_price(self, use_case, customer_many_rides):
        """Test calculation with high base price."""
        high_price = Decimal("1000.00")
        context = RideContext(
            customer=customer_many_rides,
            distance_km=Decimal("25"),
            base_price=high_price,
            ride_datetime=datetime(2024, 1, 10, 14, 0),
        )

        final_price, applied_discounts = use_case.execute(context)

        assert len(applied_discounts) == 3
        # Should apply discounts proportionally to higher price
        assert final_price < high_price
        assert final_price > 0
