from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Type


@dataclass
class Customer:
    id: str
    total_rides: int


@dataclass
class RideContext:
    customer: Customer
    distance_km: Decimal
    base_price: Decimal
    ride_datetime: datetime


@dataclass
class DiscountResult:
    discount_percentage: Decimal
    reason: str


class DiscountRule(ABC):
    registered_rules: ClassVar[list[Type["DiscountRule"]]] = []

    def __init_subclass__(cls):
        super().__init_subclass__()
        DiscountRule.registered_rules.append(cls)

    @abstractmethod
    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        pass


class RideFrequencyDiscountRule(DiscountRule):
    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        total_rides = context.customer.total_rides

        if total_rides == 0:
            return None

        discount = min(Decimal(total_rides // 10), Decimal("15"))

        if discount > 0:
            return DiscountResult(
                discount_percentage=discount,
                reason=f"Ride frequency discount ({total_rides} rides)"
            )


class ProportionalDistanceDiscountRule(DiscountRule):
    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        distance = context.distance_km

        if distance > 5:
            discount = min((distance - 5) * Decimal("0.5"), Decimal("20"))
            if discount > 0:
                return DiscountResult(
                    discount_percentage=discount,
                    reason=f"Distance discount ({distance}km)"
                )


class OffPeakDiscountRule(DiscountRule):
    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        current_hour = context.ride_datetime.hour

        if 0 <= current_hour < 6:
            return DiscountResult(
                discount_percentage=Decimal("20"),
                reason="Late night off-peak discount"
            )
        elif 10 <= current_hour < 16:
            if context.ride_datetime.weekday() < 5:
                return DiscountResult(
                    discount_percentage=Decimal("10"),
                    reason="Mid-day off-peak discount"
                )


class RideDiscountCalculator:
    MAX_TOTAL_DISCOUNT = Decimal("50")

    def calculate_final_price(self, context: RideContext) -> tuple[Decimal, list[DiscountResult]]:
        applied_discounts = [
            discount_result
            for rule_class in DiscountRule.registered_rules
            if (discount_result := rule_class().calculate_discount(context))
        ]

        total_discount_percentage = min(
            sum(d.discount_percentage for d in applied_discounts),
            self.MAX_TOTAL_DISCOUNT
        )

        discount_amount = context.base_price * (total_discount_percentage / 100)
        final_price = context.base_price - discount_amount

        return final_price, applied_discounts

