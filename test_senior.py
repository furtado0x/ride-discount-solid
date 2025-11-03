from decimal import Decimal
from datetime import datetime
from ride_discount_system import (
    Customer,
    RideContext,
    RideDiscountCalculator
)

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
for discount in applied_discounts:
    print(f"  - {discount.reason}: {discount.discount_percentage:.1f}%")

total_discount = sum(d.discount_percentage for d in applied_discounts)
print()
print(f"Total Discount: {min(total_discount, Decimal('50')):.1f}%")
print(f"Final Price: ${final_price:.2f}")
print(f"You saved: ${ride_context.base_price - final_price:.2f}")