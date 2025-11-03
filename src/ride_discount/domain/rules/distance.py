"""Distance-based discount rule."""

from decimal import Decimal

from ride_discount.application.dtos import RideContext
from ride_discount.domain.rules.base import DiscountRule
from ride_discount.domain.value_objects import DiscountResult


class ProportionalDistanceDiscountRule(DiscountRule):
    """Discount rule based on ride distance.

    Provides a discount for longer rides: 0.5% for each kilometer beyond 5km,
    up to a maximum of 20%.

    Formula: min((distance - 5) * 0.5, 20) for distance > 5km
    """

    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        """Calculate distance-based discount.

        Args:
            context: The ride context containing distance information

        Returns:
            DiscountResult if distance exceeds 5km, None otherwise
        """
        distance = context.distance_km

        if distance > 5:
            discount = min((distance - 5) * Decimal("0.5"), Decimal("20"))
            if discount > 0:
                return DiscountResult(
                    discount_percentage=discount,
                    reason=f"Distance discount ({distance}km)",
                )

        return None
