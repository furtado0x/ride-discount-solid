"""Ride frequency discount rule."""

from decimal import Decimal

from ride_discount.application.dtos import RideContext
from ride_discount.domain.rules.base import DiscountRule
from ride_discount.domain.value_objects import DiscountResult


class RideFrequencyDiscountRule(DiscountRule):
    """Discount rule based on customer ride frequency.

    Provides a loyalty discount: 1% for every 10 rides completed,
    up to a maximum of 15%.

    Formula: min(total_rides // 10, 15)
    """

    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        """Calculate frequency-based discount.

        Args:
            context: The ride context containing customer information

        Returns:
            DiscountResult if customer has completed rides, None otherwise
        """
        total_rides = context.customer.total_rides

        if total_rides == 0:
            return None

        discount = min(Decimal(total_rides // 10), Decimal("15"))

        if discount > 0:
            return DiscountResult(
                discount_percentage=discount,
                reason=f"Ride frequency discount ({total_rides} rides)",
            )

        return None
