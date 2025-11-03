#!/usr/bin/env python3
"""Demo script showing the ride discount system in action."""

import sys
from datetime import datetime
from decimal import Decimal

sys.path.insert(0, "src")

from ride_discount import (
    CalculateRideDiscountUseCase,
    Customer,
    RideContext,
)


def print_separator():
    """Print a visual separator."""
    print("\n" + "=" * 80 + "\n")


def main():
    """Run the ride discount calculation demo."""
    print_separator()
    print("🚗 RIDE DISCOUNT SYSTEM - Clean Architecture Demo")
    print_separator()

    # Create use case
    use_case = CalculateRideDiscountUseCase()

    # Example 1: No discounts
    print("📊 Example 1: New customer, short ride, rush hour")
    customer1 = Customer(id="CUST-001", total_rides=0)
    context1 = RideContext(
        customer=customer1,
        distance_km=Decimal("3"),
        base_price=Decimal("100.00"),
        ride_datetime=datetime(2024, 1, 10, 8, 0),  # Rush hour
    )

    final_price1, discounts1 = use_case.execute(context1)
    print(f"  Base price: ${context1.base_price}")
    print(f"  Discounts applied: {len(discounts1)}")
    print(f"  Final price: ${final_price1}")

    # Example 2: Multiple discounts
    print_separator()
    print("📊 Example 2: Loyal customer, long ride, midday weekday")
    customer2 = Customer(id="CUST-002", total_rides=75)
    context2 = RideContext(
        customer=customer2,
        distance_km=Decimal("25"),
        base_price=Decimal("100.00"),
        ride_datetime=datetime(2024, 1, 10, 14, 0),  # Midday Wednesday
    )

    final_price2, discounts2 = use_case.execute(context2)
    print(f"  Base price: ${context2.base_price}")
    print(f"  Discounts applied: {len(discounts2)}")
    for discount in discounts2:
        print(f"    • {discount.reason}: {discount.discount_percentage}%")
    total_discount = sum(d.discount_percentage for d in discounts2)
    print(f"  Total discount: {total_discount}%")
    print(f"  Final price: ${final_price2}")

    # Example 3: Maximum discount cap
    print_separator()
    print("📊 Example 3: Super loyal customer, very long ride, late night")
    customer3 = Customer(id="CUST-003", total_rides=200)
    context3 = RideContext(
        customer=customer3,
        distance_km=Decimal("100"),
        base_price=Decimal("100.00"),
        ride_datetime=datetime(2024, 1, 10, 3, 0),  # Late night
    )

    final_price3, discounts3 = use_case.execute(context3)
    print(f"  Base price: ${context3.base_price}")
    print(f"  Discounts applied: {len(discounts3)}")
    for discount in discounts3:
        print(f"    • {discount.reason}: {discount.discount_percentage}%")
    total_discount_raw = sum(d.discount_percentage for d in discounts3)
    print(f"  Total discount (raw): {total_discount_raw}%")
    print(f"  Total discount (capped): {min(total_discount_raw, Decimal('50'))}%")
    print(f"  Final price: ${final_price3}")

    print_separator()
    print("✅ Demo completed successfully!")
    print_separator()


if __name__ == "__main__":
    main()
