"""Off-peak hours discount rule."""

from decimal import Decimal

from ride_discount.application.dtos import RideContext
from ride_discount.domain.rules.base import DiscountRule
from ride_discount.domain.value_objects import DiscountResult


class OffPeakDiscountRule(DiscountRule):
    """Discount rule for off-peak riding hours.

    Provides discounts for rides during less busy times:
    - Late night (0-6h): 20% discount
    - Mid-day weekdays (10-16h): 10% discount
    """

    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        """Calculate off-peak hours discount.

        Args:
            context: The ride context containing datetime information

        Returns:
            DiscountResult if ride occurs during off-peak hours, None otherwise
        """
        current_hour = context.ride_datetime.hour

        if 0 <= current_hour < 6:
            return DiscountResult(
                discount_percentage=Decimal("20"),
                reason="Late night off-peak discount",
            )
        elif 10 <= current_hour < 16 and context.ride_datetime.weekday() < 5:
            return DiscountResult(
                discount_percentage=Decimal("10"),
                reason="Mid-day off-peak discount",
            )

        return None
