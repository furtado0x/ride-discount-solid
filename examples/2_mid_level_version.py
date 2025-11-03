from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Customer:
    id: str
    total_rides: int


@dataclass
class RideInfo:
    customer: Customer
    distance_km: Decimal
    base_price: Decimal
    ride_datetime: datetime


@dataclass
class DiscountInfo:
    percentage: Decimal
    description: str


class RideDiscountCalculator:
    MAX_DISCOUNT = Decimal("50")

    def calculate_frequency_discount(self, ride: RideInfo) -> DiscountInfo | None:
        total_rides = ride.customer.total_rides

        if total_rides > 0:
            discount = min(Decimal(total_rides // 10), Decimal("15"))
            if discount > 0:
                return DiscountInfo(
                    percentage=discount,
                    description=f"Ride frequency discount ({total_rides} rides)"
                )
        return None

    def calculate_distance_discount(self, ride: RideInfo) -> DiscountInfo | None:
        distance = ride.distance_km

        if distance > 5:
            discount = min((distance - 5) * Decimal("0.5"), Decimal("20"))
            if discount > 0:
                return DiscountInfo(
                    percentage=discount,
                    description=f"Distance discount ({distance}km)"
                )
        return None

    def calculate_offpeak_discount(self, ride: RideInfo) -> DiscountInfo | None:
        current_hour = ride.ride_datetime.hour

        if 0 <= current_hour < 6:
            return DiscountInfo(
                percentage=Decimal("20"),
                description="Late night off-peak discount"
            )
        elif 10 <= current_hour < 16 and ride.ride_datetime.weekday() < 5:
            return DiscountInfo(
                percentage=Decimal("10"),
                description="Mid-day off-peak discount"
            )
        return None

    def calculate_final_price(self, ride: RideInfo):
        all_discounts = []

        frequency_discount = self.calculate_frequency_discount(ride)
        if frequency_discount:
            all_discounts.append(frequency_discount)

        distance_discount = self.calculate_distance_discount(ride)
        if distance_discount:
            all_discounts.append(distance_discount)

        offpeak_discount = self.calculate_offpeak_discount(ride)
        if offpeak_discount:
            all_discounts.append(offpeak_discount)

        total_discount_percentage = sum(d.percentage for d in all_discounts)
        total_discount_percentage = min(total_discount_percentage, self.MAX_DISCOUNT)

        discount_amount = ride.base_price * (total_discount_percentage / 100)
        final_price = ride.base_price - discount_amount

        return final_price, all_discounts


if __name__ == "__main__":
    customer = Customer(id="usr_123", total_rides=75)

    ride = RideInfo(
        customer=customer,
        distance_km=Decimal("25"),
        base_price=Decimal("45.00"),
        ride_datetime=datetime(2024, 3, 15, 14, 30)
    )

    calculator = RideDiscountCalculator()
    final_price, discounts = calculator.calculate_final_price(ride)

    print("Ride Details:")
    print(f"  Total Rides: {ride.customer.total_rides}")
    print(f"  Distance: {ride.distance_km} km")
    print(f"  Base Price: ${ride.base_price}")
    print(f"  Date/Time: {ride.ride_datetime.strftime('%Y-%m-%d %H:%M')}")
    print()

    print("Applied Discounts:")
    for discount in discounts:
        print(f"  - {discount.description}: {discount.percentage:.1f}%")

    total_discount = sum(d.percentage for d in discounts)
    print()
    print(f"Total Discount: {min(total_discount, Decimal('50')):.1f}%")
    print(f"Final Price: ${final_price:.2f}")
    print(f"You saved: ${ride.base_price - final_price:.2f}")