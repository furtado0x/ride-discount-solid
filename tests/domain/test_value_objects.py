"""Tests for domain value objects."""

from decimal import Decimal

import pytest

from ride_discount.domain.value_objects import DiscountResult


class TestDiscountResult:
    """Tests for DiscountResult value object."""

    def test_create_discount_result_with_valid_data(self):
        """Test creating a discount result with valid data."""
        result = DiscountResult(
            discount_percentage=Decimal("10"), reason="Test discount"
        )
        assert result.discount_percentage == Decimal("10")
        assert result.reason == "Test discount"

    def test_discount_result_is_immutable(self):
        """Test that discount result is immutable (frozen)."""
        result = DiscountResult(
            discount_percentage=Decimal("10"), reason="Test discount"
        )
        with pytest.raises(AttributeError):
            result.discount_percentage = Decimal("20")  # type: ignore

    def test_discount_result_with_zero_percentage(self):
        """Test creating a discount result with zero percentage."""
        result = DiscountResult(discount_percentage=Decimal("0"), reason="No discount")
        assert result.discount_percentage == Decimal("0")

    def test_discount_result_with_negative_percentage_raises_error(self):
        """Test that negative percentage raises ValueError."""
        with pytest.raises(ValueError, match="discount_percentage must be non-negative"):
            DiscountResult(discount_percentage=Decimal("-1"), reason="Invalid")

    def test_discount_result_with_percentage_over_100_raises_error(self):
        """Test that percentage over 100 raises ValueError."""
        with pytest.raises(ValueError, match="discount_percentage cannot exceed 100"):
            DiscountResult(discount_percentage=Decimal("101"), reason="Invalid")

    @pytest.mark.parametrize(
        "percentage,reason",
        [
            (Decimal("0"), "No discount"),
            (Decimal("10"), "Basic discount"),
            (Decimal("50"), "Half price"),
            (Decimal("100"), "Free ride"),
        ],
    )
    def test_discount_result_with_various_valid_percentages(self, percentage, reason):
        """Test discount result creation with various valid percentages."""
        result = DiscountResult(discount_percentage=percentage, reason=reason)
        assert result.discount_percentage == percentage
        assert result.reason == reason
