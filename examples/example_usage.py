from decimal import Decimal
from datetime import datetime

from ride_discount_system import (
    Customer,
    RideContext,
    RideDiscountCalculator,
    DiscountRule,
    DiscountResult
)


def demonstrate_discount_system():
    customer = Customer(
        id="usr_123",
        total_rides=75
    )

    ride_context = RideContext(
        customer=customer,
        distance_km=Decimal("25"),
        base_price=Decimal("45.00"),
        ride_datetime=datetime(2024, 3, 15, 14, 30)
    )

    calculator = RideDiscountCalculator()
    final_price, applied_discounts = calculator.calculate_final_price(ride_context)

    print("Ride Details:")
    print(f"  Total Rides: {ride_context.customer.total_rides}")
    print(f"  Distance: {ride_context.distance_km} km")
    print(f"  Base Price: ${ride_context.base_price}")
    print(f"  Date/Time: {ride_context.ride_datetime.strftime('%Y-%m-%d %H:%M')}")
    print()

    print("Applied Discounts:")
    total_discount = Decimal("0")
    for discount in applied_discounts:
        print(f"  - {discount.reason}: {discount.discount_percentage:.1f}%")
        total_discount += discount.discount_percentage

    print()
    print(f"Total Discount: {min(total_discount, Decimal('50')):.1f}%")
    print(f"Final Price: ${final_price:.2f}")
    print(f"You saved: ${ride_context.base_price - final_price:.2f}")


def demonstrate_extensibility():
    print("\n" + "="*60)
    print("DEMONSTRATING OPEN/CLOSED PRINCIPLE")
    print("="*60)

    initial_rules = len(DiscountRule.registered_rules)
    print(f"\nNumber of discount rules before: {initial_rules}")
    print("Current rules:")
    for rule in DiscountRule.registered_rules:
        print(f"  - {rule.__name__}")

    print("\nAdding a new discount rule WITHOUT modifying existing code...")

    class MilestoneDiscountRule(DiscountRule):
        def calculate_discount(self, context: RideContext) -> DiscountResult | None:
            total_rides = context.customer.total_rides
            milestones = [10, 25, 50, 100, 250, 500, 1000]

            if total_rides in milestones:
                return DiscountResult(
                    discount_percentage=Decimal("5"),
                    reason=f"Milestone bonus! {total_rides}th ride"
                )
            return None

    print(f"\nNumber of discount rules after: {len(DiscountRule.registered_rules)}")
    print("Current rules:")
    for rule in DiscountRule.registered_rules:
        print(f"  - {rule.__name__}")

    print("\n✅ New rule added without modifying ANY existing code!")
    print("   The system is OPEN for extension but CLOSED for modification!")


if __name__ == "__main__":
    demonstrate_discount_system()
    demonstrate_extensibility()
