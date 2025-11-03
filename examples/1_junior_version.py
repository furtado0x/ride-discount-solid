from decimal import Decimal
from datetime import datetime


def calculate_ride_price(total_rides, distance_km, base_price, ride_datetime):
    total_discount = Decimal("0")
    discounts_applied = []

    if total_rides > 0:
        frequency_discount = min(Decimal(total_rides // 10), Decimal("15"))
        if frequency_discount > 0:
            total_discount += frequency_discount
            discounts_applied.append(f"Ride frequency discount ({total_rides} rides): {frequency_discount}%")

    if distance_km > 5:
        distance_discount = min((distance_km - 5) * Decimal("0.5"), Decimal("20"))
        if distance_discount > 0:
            total_discount += distance_discount
            discounts_applied.append(f"Distance discount ({distance_km}km): {distance_discount:.1f}%")

    current_hour = ride_datetime.hour
    if 0 <= current_hour < 6:
        total_discount += Decimal("20")
        discounts_applied.append("Late night off-peak discount: 20%")
    elif 10 <= current_hour < 16 and ride_datetime.weekday() < 5:
        total_discount += Decimal("10")
        discounts_applied.append("Mid-day off-peak discount: 10%")

    if total_discount > 50:
        total_discount = Decimal("50")

    discount_amount = base_price * (total_discount / 100)
    final_price = base_price - discount_amount

    return final_price, discounts_applied, total_discount


if __name__ == "__main__":
    total_rides = 75
    distance_km = 25
    base_price = Decimal("45.00")
    ride_datetime = datetime(2024, 3, 15, 14, 30)

    final_price, discounts, total_discount = calculate_ride_price(
        total_rides, distance_km, base_price, ride_datetime
    )

    print("Ride Details:")
    print(f"  Total Rides: {total_rides}")
    print(f"  Distance: {distance_km} km")
    print(f"  Base Price: ${base_price}")
    print(f"  Date/Time: {ride_datetime.strftime('%Y-%m-%d %H:%M')}")
    print()

    print("Applied Discounts:")
    for discount in discounts:
        print(f"  - {discount}")

    print()
    print(f"Total Discount: {total_discount}%")
    print(f"Final Price: ${final_price:.2f}")
    print(f"You saved: ${base_price - final_price:.2f}")