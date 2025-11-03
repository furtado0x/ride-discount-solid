"""Tests for domain entities."""

import pytest

from ride_discount.domain.entities import Customer


class TestCustomer:
    """Tests for Customer entity."""

    def test_create_customer_with_valid_data(self):
        """Test creating a customer with valid data."""
        customer = Customer(id="CUST-001", total_rides=10)
        assert customer.id == "CUST-001"
        assert customer.total_rides == 10

    def test_customer_is_immutable(self):
        """Test that customer entity is immutable (frozen)."""
        customer = Customer(id="CUST-001", total_rides=10)
        with pytest.raises(AttributeError):
            customer.total_rides = 20  # type: ignore

    def test_customer_with_zero_rides(self):
        """Test creating a customer with zero rides."""
        customer = Customer(id="CUST-001", total_rides=0)
        assert customer.total_rides == 0

    def test_customer_with_negative_rides_raises_error(self):
        """Test that negative total_rides raises ValueError."""
        with pytest.raises(ValueError, match="total_rides must be non-negative"):
            Customer(id="CUST-001", total_rides=-1)

    @pytest.mark.parametrize(
        "customer_id,total_rides",
        [
            ("CUST-001", 0),
            ("CUST-002", 25),
            ("CUST-003", 100),
            ("CUST-004", 1000),
        ],
    )
    def test_customer_creation_with_various_values(self, customer_id, total_rides):
        """Test customer creation with various valid values."""
        customer = Customer(id=customer_id, total_rides=total_rides)
        assert customer.id == customer_id
        assert customer.total_rides == total_rides
